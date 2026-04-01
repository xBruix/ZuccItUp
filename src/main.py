from server import Server
from menu import Menu
from order import Order, Cart, Status
from user import User, Customer, DeliveryAgent
from notification import Notification
from getpass import getpass		# for typing password without showing letters
import sys						# to exit program
import re						# for regex
from datetime import datetime
from prettytable import PrettyTable

#whereever "logout" is typed, it passes this and goes back to login
class LogoutException(Exception):
    pass


#DB
print("Welcome to Zucc It Up!\n")
print("Type 'quit' at any time to exit, or 'logout' to log out of your account.\n")
 
mango_username = input("Enter your MangoDB username: ")
mango_password = getpass("Enter your MangoDB password: ")
 
try:
    server = Server(user_id=mango_username, passwd=mango_password)
except ValueError as e:
    print(f"\nCould not connect to the database: {e}")
    print("Please check your credentials and try again.")
    sys.exit(1)
 
    #A single User object persists across login/logout cycles
user = User(server)
#DB end


#input function helpers
#logout checker
def check_logout_or_quit(answer: str) -> str:
    if answer.lower() == "quit":
        server.disconnect()
        sys.exit(0)
    elif answer.lower() == "logout":
        raise LogoutException()
    return answer

#string input
def input_str(msg: str, regex_pattern: str = None) -> str:
    if regex_pattern is None:
        return check_logout_or_quit(input(msg))
 
    while True:
        answer = check_logout_or_quit(input(msg))
        if re.match(regex_pattern, answer):
            return answer
        print("Sorry, that was not a valid answer. Please try again.")

#integer input
def input_int(msg: str, minimum: int = -sys.maxsize - 1, maximum: int = sys.maxsize) -> int:
    while True:
        raw = check_logout_or_quit(input(msg))
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Please enter a number between {minimum} and {maximum}.")
#end of input



# Login / Signup
def login_or_signup():
    while True:
        option = input_int(
            "\n" + "-" * 20 + "\n 1. Login\n  2. Sign Up\n> ",
            1, 2
        )
 
        if option == 1:
            viu_id   = input_str("VIU ID (9 digits)\n> ", r"^[0-9]{9}$")
            password = getpass("Password\n> ")
            if user.login(viu_id, password):
                print(f"\nWelcome back, {user.get_name()}!")
                return
            print("Incorrect VIU ID or password. Please try again.")
 
        else:
            role_opt = input_int("Role:\n  1. Customer\n  2. Delivery Agent\n> ", 1, 2)
            role     = "Customer" if role_opt == 1 else "Agent"
            viu_id   = input_str("VIU ID (9 digits)\n> ", r"^[0-9]{9}$")
            password = getpass("Choose a password\n> ")
            name     = input_str("Your name\n> ")
            email    = input_str(
                "Your email\n> ",
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            )
            if user.signup(viu_id=viu_id, passwd=password, name=name, email=email, role=role):
                print(f"\nAccount created! Welcome, {user.get_name()}!")
                return
            print("Sign-up failed. That VIU ID may already be in use. Please try again.")
#end of login
 
#Ordering flow
def ordering_flow(user_obj):
    """
    Full ordering experience:
      1. Enter delivery location
      2. Loop: browse vendors and add items  OR  view cart / checkout
    user_obj must expose get_name() — works for both Customer and DeliveryAgent.
    """
    print("\n" + "─" * 45)
    print("  Set your delivery location.")
    building = input_str("Building number (e.g. 315)\n> ", r"^[1-4]\d\d$")
    room     = input_str("Room number (e.g. 114)\n> ",     r"^[1-5]\d\d\w?$")
    cart     = Cart(building, room, server)
    menu_obj = Menu(type="", schedule=[], publishStatus=True, server=server)
 
    while True:
        # Step 2.2: main ordering choice
        print("\n" + "─" * 45)
        print("  1. Browse vendors and add items")
        print("  2. View cart")
        print("  0. Cancel and go back")
        print("─" * 45)
        choice = input_int("Enter choice\n> ", 0, 2)
 
        if choice == 0:
            return
        elif choice == 1:
            _browse_and_add(menu_obj, cart)    # Steps 2.3–2.8
        elif choice == 2:
            done = _cart_and_checkout(user_obj, cart)    # Steps 2.9–2.11
            if done:
                return    # Order placed; go back to caller's main menu

def _browse_and_add(menu_obj: Menu, cart: Cart):
    """
    Steps 2.3-2.8: List vendors → select → list menus → select → list items → add.
    Returns to the ordering_flow loop after one item is added.
    """
    # Step 2.3: List vendors
    vendors = server.view_all_users("Vendor")
    if not vendors:
        print("No vendors are currently available.")
        return
 
    vendor_table = PrettyTable()
    vendor_table.align = "l"
    vendor_table.field_names = ["#", "Vendor", "Location", "Hours", "Open Now"]
    now_str = datetime.now().strftime("%H:%M")
    for i, v in enumerate(vendors, 1):
        hrs = v.get("hoursOfOperation", {})
        open_flag = "Yes" if hrs.get("startTime","") <= now_str <= hrs.get("endTime","") else "No"
        hours_str = f"{hrs.get('days','')} {hrs.get('startTime','')}–{hrs.get('endTime','')}"
        vendor_table.add_row([i, v["name"], v.get("location",""), hours_str, open_flag])
    print(vendor_table)
 
    # Step 2.4: Customer selects vendor
    vendor_num = input_int("Select vendor # (or 0 to cancel)\n> ", 0, len(vendors))
    if vendor_num == 0:
        return
    vendor_name = vendors[vendor_num - 1]["name"]
 
    # Step 2.5: List menus for that vendor
    menus = menu_obj.get_menus_for_vendor(vendor_name)
    if not menus:
        print(f"No menus available for {vendor_name}.")
        return
 
    print(f"\nMenus available at {vendor_name}:")
    for i, m in enumerate(menus, 1):
        sched = m.get("schedule", {})
        if isinstance(sched, dict):
            sched_str = f"{sched.get('days','')} {sched.get('startTime','')}–{sched.get('endTime','')}"
        else:
            sched_str = str(sched)
        print(f"  {i}. [{m.get('type','?')} Menu]  {sched_str}")
 
    # Step 2.6: Customer selects a menu
    menu_num = input_int("Select menu # (or 0 to cancel)\n> ", 0, len(menus))
    if menu_num == 0:
        return
    selected_menu = menus[menu_num - 1]
    menu_type = selected_menu.get("type", "")
 
    # Step 2.7: List items from that menu
    items = menu_obj.get_items_for_menu(vendor_name, menu_type)
    if not items:
        print("No items are available in this menu.")
        return
 
    print(f"\n{'#':<4} {'Name':<25} {'Price':>8}  {'In Stock':<10}  Description")
    print("─" * 75)
    for i, item in enumerate(items, 1):
        stock = "Yes" if item.get("inStock") else "No"
        print(
            f"{i:<4} {item.get('name',''):<25} "
            f"${item.get('price',0):>7.2f}  "
            f"{stock:<10}  "
            f"{item.get('description','')}"
        )
 
    # Step 2.8: Select item
    item_num = input_int("Select item # (or 0 to cancel)\n> ", 0, len(items))
    if item_num == 0:
        return
 
    selected_item = items[item_num - 1]
    if not selected_item.get("inStock"):
        print("Sorry, that item is currently out of stock.")
        return
 
    # Step 2.8b: Select quantity
    quantity = input_int("Enter quantity\n> ", 1, 99)
    cart.add_to_cart(selected_item["name"], quantity)
    # Returns to ordering_flow loop → customer sees "Browse vendors" or "View cart" again (Step 2.2)
 
 
def _cart_and_checkout(user_obj, cart: Cart) -> bool:
    """
    Steps 2.9-2.11: Show cart → choose to go back to vendors or checkout.
    Returns True if orders were placed (so caller resets the cart state).
    """
    if cart.num_items() == 0:
        print("\nYour cart is empty. Add some items first.")
        return False
 
    # Step 2.9: List cart info
    cart.view_cart()
    subtotal = cart.calculate_subtotal()
    print(f"\nEstimated total: ${subtotal:.2f}")
 
    # Step 2.10: Back to vendors or proceed to checkout
    print("\n  1. Back to browsing vendors")
    print("  2. Proceed to checkout")
    choice = input_int("Enter choice\n> ", 1, 2)
    if choice == 1:
        return False
 
    # Step 2.11: Customer places order
    instructions = input_str("Special instructions (press Enter to skip)\n> ")
 
    # Convert cart → one Order per vendor (spec: "potentially multiple orders")
    orders = cart.convert_to_orders(user_obj.get_current_user(), instructions)
    if not orders:
        print("No orders to place.")
        return False
 
    # Summary before confirming
    print(f"\nYou are placing {len(orders)} order(s):")
    for o in orders:
        print(f"  • {o.get_vendor():<22}  ${o.get_subtotal():.2f}")
 
    confirm = input_str("Confirm? (y/n)\n> ")
    if confirm.lower() != "y":
        print("Order cancelled.")
        return False
 
    # Place each order and send its notification
    for o in orders:
        if o.place_order():
            print(f"  ✓ Order placed with {o.get_vendor()} (ID: {o.get_order_id()})")
            notif = Notification("", "", user_obj.get_current_user(), server, o.get_order_id())
            notif.sendNotification()
 
    return True    # Signal to caller that ordering is done
#ordering ends


#Customer flow
def run_customer():
    """Main loop for the Customer role."""
    customer = Customer(server, user)
    print(f"\n  Welcome, {customer.get_name()}!")
 
    while True:
        print("\n" + "─" * 45)
        print("  Customer Menu")
        print("─" * 45)
        print("  1. Place an order")
        print("  2. View my orders")
        print("  3. Confirm order received")
        print("  4. View notifications")
        print("  5. View my profile")
        print("  0. Logout")
        print("─" * 45)
        choice = input_int("Enter choice\n> ", 0, 5)
 
        if choice == 0:
            raise LogoutException()
        elif choice == 1:
            ordering_flow(customer)                            # Steps 2.1–2.11
        elif choice == 2:
            _view_customer_orders(customer)
        elif choice == 3:
            _confirm_received_flow(customer)                   # Step 2.13
        elif choice == 4:
            _view_customer_notifications(customer)             # Step 2.12
        elif choice == 5:
            customer.viewCustomer()
 
 
def _view_customer_orders(customer: Customer):
    """Display all orders placed by this customer."""
    my_orders = [
        o for o in server.get_all_orders()
        if o.get("customer") == customer.get_name()
    ]
    if not my_orders:
        print("\nYou have no order history.")
        return
 
    print(f"\n{'Vendor':<22} {'Status':<18} {'Subtotal':>10}  Location")
    print("─" * 65)
    for o in my_orders:
        loc = f"Bldg {o.get('building','?')}, Rm {o.get('room','?')}"
        print(
            f"{o.get('vendor',''):<22} "
            f"{o.get('orderStatus',''):<18} "
            f"${o.get('subTotal',0.0):>9.2f}  "
            f"{loc}"
        )
 
 
def _confirm_received_flow(customer: Customer):
    """
    Step 2.13: Show orders with status Delivered and let the customer
    confirm receipt, which changes the status to Received.
    """
    delivered = [
        o for o in server.get_all_orders()
        if o.get("customer") == customer.get_name()
        and o.get("orderStatus") == Status.DELIVERED.value
    ]
    if not delivered:
        print("\nNo orders are awaiting your confirmation.")
        return
 
    print(f"\n{'#':<4} {'Vendor':<22} {'Subtotal':>10}  Location")
    print("─" * 50)
    for i, o in enumerate(delivered, 1):
        loc = f"Bldg {o.get('building','?')}, Rm {o.get('room','?')}"
        print(f"{i:<4} {o.get('vendor',''):<22} ${o.get('subTotal',0.0):>9.2f}  {loc}")
 
    num = input_int("Select order # to confirm receipt (or 0 to cancel)\n> ", 0, len(delivered))
    if num == 0:
        return
 
    doc = delivered[num - 1]
    order = Order(
        svr=server,
        building=doc.get("building",""),
        room=doc.get("room",""),
        total=doc.get("subTotal",0.0),
        instructions=doc.get("specialInstructions",""),
        customer=doc.get("customer",""),
        vendor=doc.get("vendor",""),
    )
    order.set_order_id(str(doc["_id"]))
    order.set_status(doc.get("orderStatus",""))
    order.confirm_received()    # Step 2.13: status → Received
 
 
def _view_customer_notifications(customer: Customer):
    """
    Step 2.12: Show order status notifications for all customer orders.
    Notification messages are derived from live order status — no DB collection needed.
    """
    notif = Notification("", "", customer.get_name(), server)
    notif.viewNotification()
#customer flow ends
 

# DELIVERY AGENT FLOW
def run_agent():
    """Main loop for the Delivery Agent role."""
    agent = DeliveryAgent(server, user)
    avail_label = "Available" if agent.get_availability_status() else "Unavailable"
    print(f"\n  Welcome, {agent.get_name()}!  ({avail_label})")
 
    while True:
        print("\n" + "─" * 45)
        print("  Delivery Agent Menu")
        print("─" * 45)
        print("  1. Order food")
        print("  2. View my active orders")
        print("  3. Set my availability")
        print("  4. View available deliveries")
        print("  5. View my profile")
        print("  6. View notifications")
        print("  0. Logout")
        print("─" * 45)
        choice = input_int("Enter choice\n> ", 0, 6)
 
        if choice == 0:
            raise LogoutException()
        elif choice == 1:
            ordering_flow(agent)                               # Step 3.1: agent acts as customer
        elif choice == 2:
            _view_agent_active_orders(agent)                   # Step 3.2
        elif choice == 3:
            _set_agent_availability(agent)                     # Step 3.3
        elif choice == 4:
            _view_available_deliveries(agent)                  # Step 3.4
        elif choice == 5:
            agent.viewAgent()
        elif choice == 6:
            _view_agent_notifications(agent)
 
 
def _set_agent_availability(agent: DeliveryAgent):
    """Step 3.3: Toggle the agent's availability status."""
    current = agent.get_availability_status()
    print(f"\nYou are currently {'available' if current else 'unavailable'}.")
    choice = input_str("Change status? (y/n)\n> ")
    if choice.lower() == "y":
        agent.setAvailability(not current)
 
 
def _view_agent_active_orders(agent: DeliveryAgent):
    """
    Step 3.2: List orders the agent has accepted (ReadyForPickup or InTransit).
    Step 3.2.2: Agent selects one and can manage it (mark picked up / mark delivered).
    """
    active = [
        o for o in server.get_all_orders()
        if o.get("agent") == agent.get_name()
        and o.get("orderStatus") in [Status.READY_FOR_PICKUP.value, Status.IN_TRANSIT.value]
    ]
    if not active:
        print("\nYou have no active orders.")
        return
 
    print(f"\n{'#':<4} {'Customer':<15} {'Vendor':<20} {'Status':<18} Location")
    print("─" * 75)
    for i, o in enumerate(active, 1):
        loc = f"Bldg {o.get('building','?')}, Rm {o.get('room','?')}"
        print(
            f"{i:<4} {o.get('customer',''):<15} "
            f"{o.get('vendor',''):<20} "
            f"{o.get('orderStatus',''):<18} "
            f"{loc}"
        )
 
    num = input_int("Select order # to manage (or 0 to cancel)\n> ", 0, len(active))
    if num == 0:
        return
 
    _manage_order_in_progress(agent, active[num - 1])
 
 
def _view_available_deliveries(agent: DeliveryAgent):
    """
    Step 3.4: Show pending (unassigned) orders. Agent can accept or decline.
    If available, agent goes through: accept → pick up → deliver.
    """
    # Step 3.4.1: Check availability
    if not agent.get_availability_status():
        print("\nYou are set as unavailable. Use option 3 to make yourself available first.")
        return
 
    while True:
        # Step 3.4.2: Refresh available deliveries each loop
        pending = [
            o for o in server.get_all_orders()
            if o.get("orderStatus") == Status.PENDING.value
        ]
        if not pending:
            print("\nNo deliveries are available right now.")
            return
 
        # Step 3.4.3: Show delivery info
        print(f"\n{'#':<4} {'Customer':<15} {'Vendor':<22} {'Building':<10} {'Room':<6} Subtotal")
        print("─" * 75)
        for i, o in enumerate(pending, 1):
            print(
                f"{i:<4} {o.get('customer',''):<15} "
                f"{o.get('vendor',''):<22} "
                f"{o.get('building',''):<10} "
                f"{o.get('room',''):<6} "
                f"${o.get('subTotal',0.0):.2f}"
            )
 
        num = input_int("Select # to view details (or 0 to go back)\n> ", 0, len(pending))
        if num == 0:
            return
 
        selected = pending[num - 1]
        print(f"\n  Vendor:      {selected.get('vendor','')}")
        print(f"  Customer:    {selected.get('customer','')}")
        print(f"  Deliver to:  Bldg {selected.get('building','')}, Rm {selected.get('room','')}")
        items = selected.get("cartItem", [])
        print(f"  Items:       {len(items)} item type(s)")
        for ci in items:
            print(f"               • {ci.get('name',''):<25} x{ci.get('qty',1)}")
        print(f"  Subtotal:    ${selected.get('subTotal',0.0):.2f}")
        if selected.get("specialInstructions"):
            print(f"  Note:        {selected['specialInstructions']}")
 
        # Step 3.4.4: Accept or decline
        decision = input_int("\n  1. Accept\n  2. Decline\n  3. Back to delivery list\n> ", 1, 3)
 
        if decision == 3:
            return
 
        if decision == 2:
            # Step 3.4.5: Declined — loop back to show available deliveries
            print("Delivery declined.")
            continue
 
        # Step 3.4.6: Accepted
        order_id = str(selected["_id"])
        order = Order(
            svr=server,
            building=selected.get("building",""),
            room=selected.get("room",""),
            total=selected.get("subTotal",0.0),
            instructions=selected.get("specialInstructions",""),
            customer=selected.get("customer",""),
            vendor=selected.get("vendor",""),
        )
        order.set_order_id(order_id)
        order.set_status(selected.get("orderStatus", ""))
 
        order.accept_order(agent.get_name())    # Status → ReadyForPickup, acceptTime set
        _send_status_notification(order_id, selected.get("customer",""))
 
        print(f"\n  Deliver to: Bldg {selected.get('building')}, Rm {selected.get('room')}")
 
        # Steps 3.4.7–3.4.9: manage the delivery through pickup → delivered
        _manage_order_in_progress(agent, selected)
        return    # After delivery completes, return to agent main menu
 
 
def _manage_order_in_progress(agent: DeliveryAgent, order_doc: dict):
    """
    Steps 3.4.7-3.4.9 and 3.2.2:
    Manage an accepted order through the pickup and delivery stages.
    The order status is refreshed from the DB each loop to always show live state.
    """
    order_id = str(order_doc["_id"])
 
    # Reconstruct the Order object so we can call business-layer methods
    order = Order(
        svr=server,
        building=order_doc.get("building",""),
        room=order_doc.get("room",""),
        total=order_doc.get("subTotal",0.0),
        instructions=order_doc.get("specialInstructions",""),
        customer=order_doc.get("customer",""),
        vendor=order_doc.get("vendor",""),
    )
    order.set_order_id(order_id)
 
    while True:
        # Always fetch fresh status from DB so we reflect any external changes
        fresh_doc = server.get_order_by_id(order_id)
        if not fresh_doc:
            print("Order not found.")
            return
        current_status = fresh_doc.get("orderStatus","")
        order.set_status(current_status)
 
        print(f"\n  {order_doc.get('vendor','')} → Bldg {order_doc.get('building','')}, Rm {order_doc.get('room','')}")
        print(f"  Customer: {order_doc.get('customer','')}  |  Status: {current_status}")
        print("─" * 45)
 
        # Build the option list based on current status
        options = []
        if current_status == Status.READY_FOR_PICKUP.value:
            options.append("Mark as Picked Up")    # Step 3.4.7
        if current_status == Status.IN_TRANSIT.value:
            options.append("Mark as Delivered")    # Step 3.4.8
        options.append("View all my active orders")
        options.append("Back to main menu")
 
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
 
        choice = input_int("Enter choice\n> ", 1, len(options))
        selected_opt = options[choice - 1]
 
        if selected_opt == "Mark as Picked Up":
            order.mark_picked_up()    # Status → InTransit
            _send_status_notification(order_id, order_doc.get("customer",""))
            # Continue loop — next iteration will show "Mark as Delivered"
 
        elif selected_opt == "Mark as Delivered":
            order.mark_delivered()    # Status → Delivered
            _send_status_notification(order_id, order_doc.get("customer",""))
            print("Delivery complete!")
            # Step 3.4.9: go back to view active orders
            _view_agent_active_orders(agent)
            return
 
        elif selected_opt == "View all my active orders":
            _view_agent_active_orders(agent)
            return
 
        else:    # Back to main menu
            return
 
 
def _send_status_notification(order_id: str, customer_name: str):
    """Build and print the status notification for a single order."""
    notif = Notification("", "", customer_name, server, order_id)
    notif.sendNotification()
 
 
def _view_agent_notifications(agent: DeliveryAgent):
    """Show notifications for all orders involving this agent."""
    notif = Notification("", "", agent.get_name(), server)
    notif.viewNotification()
#agent flow complete

#main program loop
while True:
    try:
        login_or_signup()
 
        # get_role() returns title case after login ("Customer"/"Agent"),
        # lowercase after signup ("customer"/"agent") — normalise both ways.
        role = user.get_role().lower()
 
        if role == "customer":
            run_customer()
        elif role == "agent":
            run_agent()
        else:
            print(f"Unknown role '{user.get_role()}'. Please contact an administrator.")
            user.logout()
 
    except LogoutException:
        user.logout()
        print("\nLogged out successfully.")
        print("─" * 45)
        continue    # Show login screen again
 
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        break
 
    break    # Normal exit after run_customer/run_agent return (shouldn't happen without logout)

print("Goodbye!")
print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣠⡶⠒⠒⠶⣄⣠⡴⠚⠉⠁⠀⠀⠀⠀⠀⠉⠙⠳⢦⡀⠀⠀⠀⠀⠀⠀
⢠⡏⠀⠀⠀⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢧⡀⠀⠀⠀⠀
⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⢱⠀⠀⢠⠉⢡⠀⠀⠀⠀⠀⠻⡄⠀⠀⠀
⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⣾⠄⠀⢸⣦⣾⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀
⠀⠘⢧⡀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠀⠀⠸⣿⡿⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀
⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠈⠁⡴⠶⡆⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠹⡄
⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷
⠀⠀⠀⠸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠇
⠀⠀⠀⣀⡿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡽⣿⡛⠁⠀
⠀⣠⢾⣭⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠊⠀⢠⣝⣷⡀
⢠⡏⠘⠋⠀⠀⠀⠈⠑⠦⣄⣀⠀⠀⠀⠀⠀⣀⡠⠔⠋⠀⠀⠀⠈⠛⠃⢻
⠈⠷⣤⣀⣀⣀⣀⣀⣀⣀⣀⣤⡽⠟⠛⠿⣭⣄⣀⣀⣀⣀⣀⣀⣀⣀⣤⠞
⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠀⠀⠀
""")
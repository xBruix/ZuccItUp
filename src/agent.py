# Authors: Surya Balram

from notification import Notification     #importing member functions from notification.py
from order import Order            #importing member functions from order.py
from user import DeliveryAgent



def agent_main(server):
    #call from main.py agent portal
 
    # ── Login ──────────────────────────────────────────────────────
    print("\n" + "═" * 50)
    print("  ZuccItUp — Delivery Agent Portal")
    print("═" * 50)
    
    #add password somewhere here
    viuid = input("Enter your VIUID: ").strip()
 
    #build temporary agent just to call verifyVIUID
    temp = DeliveryAgent(
        availabilityStatus=False,
        VIUID=viuid,
        name="",
        email="",
        role="Agent",
    )
    temp.server = server
    #verify id
    if not temp.verifyVIUID():
        print("No agent account found with that VIUID. Please try again.")
        return
    #check
    user_data = server.view_user(viuid)
    if user_data.get("role") != "Agent":
        print("That VIUID does not belong to an agent account.")
        return
    #now build actual user object with full info
    agent = DeliveryAgent(
        availabilityStatus=user_data.get("availabilityStatus", False),
        VIUID=user_data["VIUID"],
        name=user_data["name"],
        email=user_data["email"],
        role=user_data["role"],
    )
    agent.server = server
 
    status_label = "Available" if agent.availabilityStatus else "Unavailable"
    print(f"\nWelcome, {agent.name}!  ({status_label})")
 
    # ── Menu loop ──────────────────────────────────────────────────
    while True:
        print("\n" + "─" * 45)
        print("  What would you like to do?")
        print("─" * 45)
        print("  1. View my profile")
        print("  2. Set availability")
        print("  3. View pending orders")
        print("  4. Accept an order")
        print("  5. Mark a delivery as complete")
        print("  6. View my order history")
        print("  7. View notifications")
        print("  0. Logout")
        print("─" * 45)
 
        choice = input("Enter choice: ").strip()
 
        if choice == "1":
            agent.viewAgent()
 
        elif choice == "2":
            _set_availability(agent)
 
        elif choice == "3":
            _view_pending_orders(agent, server)
 
        elif choice == "4":
            _accept_order(agent, server)
 
        elif choice == "5":
            _mark_complete(agent, server)
 
        elif choice == "6":
            _view_order_history(agent, server)
 
        elif choice == "7":
            _view_notifications(agent, server)
 
        elif choice == "0":
            print(f"\nGoodbye, {agent.name}!")
            break
 
        else:
            print("Invalid choice. Please try again.")
 

## Notification.py
def _view_notifications(agent: DeliveryAgent, server):
    #show all status for orders with this agent
    notif = Notification(
        heading="",
        description="",
        customer_VIUID=agent.name,
        server=server,
    )
    notif.viewNotification()
    
#sendNotification
def _send_status_notification(order_id: str, customer_name: str, server):
    #build and print status for one order
    notif = Notification(
        heading="",
        description="",
        customer_VIUID=customer_name,
        server=server,
        order_id=order_id,
    )
    notif.sendNotification()

## order.py
#acceptOrder
def _accept_order(agent:DeliveryAgent , server):
    #call helper
    pending = _get_pending_orders(server)
    #check
    if not pending:
        print("\nNo pending orders available to accept.")
        return
    #call helper
    _print_order_table(pending)
    #input number
    choice = input("\nEnter # to accept (or press Enter to cancel): ").strip()
    #check
    if not choice:
        return
    #check
    if not choice.isdigit() or not (1 <= int(choice) <= len(pending)):
        print("Invalid selection.")
        return
    
    selected = pending[int(choice) - 1]
    order_id = str(selected["_id"])
 
    #reconstruct Order object so we can call accept_order() on it
    order = Order(
        building=selected.get("building", ""),
        room=selected.get("room", ""),
        total=selected.get("subTotal", 0.0),
        instructions=selected.get("specialInstructions", ""),
        customer=selected.get("customer", ""),
        vendor=selected.get("vendor", ""),
        server=server,
    )
    #getting the order id to run accept on the correct order
    order._Order__order_id = order_id
    order._Order__order_status = selected.get("orderStatus", "")
    #call order.py
    order.accept_order(agent.name)
    #print confirm
    print(
        f"\nDeliver to Building {selected.get('building')}, "
        f"Room {selected.get('room')}."
    )
    #status notification for the customer
    _send_status_notification(order_id, selected.get("customer", ""), server)

#markComplete
def _mark_complete(agent:DeliveryAgent , server):\
    #create temp to run view_all
    temp = Order(
        building="", room="", total=0.0,
        instructions="", customer="", vendor="",
        server=server,
    )
    all_orders = temp.view_all_orders()
    #getting all active orders
    active = [
        o for o in all_orders
        if o.get("agent") == agent.name and o.get("orderStatus") == "In Transit"
    ]
    #check and message
    if not active:
        print("\nYou have no active deliveries to complete.")
        return
    #display and input
    _print_order_table(active, show_subtotal=False)
    choice = input("\nEnter # to mark as delivered (or press Enter to cancel): ").strip()
    if not choice:
        return
    #check
    if not choice.isdigit() or not (1 <= int(choice) <= len(active)):
        print("Invalid selection.")
        return
 
    selected = active[int(choice) - 1]
    order_id = str(selected["_id"])
    #creat order to run mark complete
    order = Order(
        building=selected.get("building", ""),
        room=selected.get("room", ""),
        total=selected.get("subTotal", 0.0),
        instructions=selected.get("specialInstructions", ""),
        customer=selected.get("customer", ""),
        vendor=selected.get("vendor", ""),
        server=server,
    )
    #obtain real order id
    order._Order__order_id = order_id
    order._Order__order_status = selected.get("orderStatus", "")
    #call order.py
    order.mark_complete()
    #status notification for the customer
    _send_status_notification(order_id, selected.get("customer", ""), server)
    
def _view_pending_orders(agent: DeliveryAgent, server):
    #calls helper
    pending = _get_pending_orders(server)
    if not pending:
        print("\nNo pending orders at this time.")
        return
    _print_order_table(pending)

def _view_order_history(agent: DeliveryAgent, server):
    #gives the agents complete order history
    #creat object to run view_all
    temp = Order(
        building="", room="", total=0.0,
        instructions="", customer="", vendor="",
        server=server,
    )
    all_orders =temp.view_all_orders()
    my_orders = [o for o in all_orders if o.get("agent") == agent.name]
    #check and message
    if not my_orders:
        print("\nYou have no order history.")
        return
    #display all
    print(f"\n{'Customer':<15} {'Vendor':<22} {'Status':<15} {'Subtotal':>10}  Location")
    print("─" * 75)
    for o in my_orders:
        loc = f"Bldg {o.get('building', '?')}, Rm {o.get('room', '?')}"
        print(
            f"{o.get('customer', ''):<15} "
            f"{o.get('vendor', ''):<22} "
            f"{o.get('orderStatus', ''):<15} "
            f"${o.get('subTotal', 0.0):>9.2f}  "
            f"{loc}"
        )

def _set_availability(agent: DeliveryAgent):  #Logic change by KW added != "y" and added last 2 lines and changed current assignment
    #change availability
    current = agent.availabilityStatus  # True or False
    print(f"\nYou are currently  {'available' if current else 'unavailable'}.")
    choice = input("Change status? (y/n): ").strip().lower()
    if choice != "y":
        print("Availability unchanged.")
        return
    new_status = not current
    agent.setAvailability(new_status)


        
def _get_pending_orders(server) -> list:
    #find any pending orders
    #create object for view_all
    temp = Order(

        #server, #added by KW
        building="", room="", total=0.0,
        instructions="", customer="", vendor="",
        server=server,   #removed by KW
    )
    all_orders = temp.view_all_orders()
    #returns pending
    return [o for o in all_orders if o.get("orderStatus") == "Pending"]

def _print_order_table(orders: list, show_subtotal: bool = True):
    #print table of specified orders
    #prints with or without subtotal when required 
    if show_subtotal:
        print(f"\n{'#':<4} {'Customer':<15} {'Vendor':<22} {'Building':<10} {'Room':<6} Subtotal")
        print("─" * 72)
        for i, o in enumerate(orders, 1):
            print(
                f"{i:<4} {o.get('customer', ''):<15} "
                f"{o.get('vendor', ''):<22} "
                f"{o.get('building', ''):<10} "
                f"{o.get('room', ''):<6} "
                f"${o.get('subTotal', 0.0):.2f}"
            )
    else:
        print(f"\n{'#':<4} {'Customer':<15} {'Vendor':<22} {'Building':<10} Room")
        print("─" * 60)
        for i, o in enumerate(orders, 1):
            print(
                f"{i:<4} {o.get('customer', ''):<15} "
                f"{o.get('vendor', ''):<22} "
                f"{o.get('building', ''):<10} "
                f"{o.get('room', '')}"
            )
#This document will contain all the queries to be used by the application

#Displays menu types and location and items
def display_menu_type():
    
    menu_type = input("Enter the menu type (or press Enter to skip): ").strip()
    location = input("Enter location of menu (or press Enter to skip): ").strip()
    
    
    query = {}
    
    if menu_type:
        query["type"] = menu_type
    
    if location:
        query["location"] = location
    
   
    result = menu.find(query, {"type": 1, "location": 1, "menuItem":1})
    
    for doc in result:
        print(doc)
    
    return list(result)

"""
If user enters both → queries both: {"type": "Breakfast", "location": "Upper Cafe"}
If user enters only type → queries type: {"type": "Breakfast"}
If user enters only location → queries location: {"location": "Upper Cafe"}
If user enters neither → queries all: {}"""

#Display a menu item using search by name (enter the name of the food item to display)
def find_menu_item(item_name):
    """
    Search for a menu item by name across all menus
    Returns the item with price and vendor info, or None if not found
    """
    # Search all menus for the item
    result = menu.aggregate([
        {"$unwind": "$menuItem"},
        {"$match": {"menuItem.name": {"$regex": f"^{item_name}$", "$options": "i"}}},
        {"$project": {
            "name": "$menuItem.name",
            "price": "$menuItem.price",
            "inStock": "$menuItem.inStock",
            "vendor": "$vendor",
            "menuType": "$type"
        }},
        {"$limit": 1}
    ])
    
    items = list(result)
    
    if items:
        return items[0] 
    return None

#Simple order placement function will need more features such as subtotal and more qty
def place_order():
   
    customer_name = input("\nEnter your name: ").strip()
    building = input("Enter building number: ").strip()
    room = input("Enter room number: ").strip()
    
    
    cart_items = []
    
    print("\nEnter items for your order (type 'done' when finished)")
    
    while True:
        item_name = input("\nFood item name (or 'done'): ").strip()
        
        if item_name.lower() == 'done':
            if not cart_items:
                print("❌ Add at least one item!")
                continue
            break
        
        if not item_name:
            continue
        
        # Check if item exists
        menu_item = find_menu_item(item_name)
        
        if not menu_item:
            print(f"❌ '{item_name}' not found")
            continue
        
        # Add to cart
        cart_items.append({
            "name": menu_item['name'],
            "qty": 1
        })
        
        print(f"✅ Added {menu_item['name']}")
    
    # Create order
    order_doc = {
        "customer": customer_name,
        "building": building,
        "room": room,
        "specialInstructions": "",
        "orderStatus": "Pending",
        "orderTime": int(datetime.now().strftime("%H%M")),
        "cartItem": cart_items
    }
    
    # Insert order
    result = order.insert_one(order_doc)
    
    print(f"\n✅ Order placed! Order ID: {result.inserted_id}")
    
    return result.inserted_id
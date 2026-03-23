#See code plan in A6 document for details on each function

#user functions
def verify_user(viu_ID):

    is_valid = false

    result = user.find_one({
        "VIUID": viu_ID
    })

    if result:
        is_valid = true
        return is_valid
    
    return is_valid
    

def create_user(email,name,viu_ID,role):

    return

def deactivate_user(viu_ID):
    result = user.update({"VIUID":""})
    return

def view_user(viu_ID):

    result = user.find_one({
        "VIUID": viu_ID
    })

    return result


#menu functions 
def get_vendors():
    return

def get_all_menu(vendorID):

    return

def get_one_menu(menuID):

    return

def get_menu_item(menuItemID):

    return

#order functions
def create_order(building,room,subtotal,instructions,customer,vendor,cart):

    return

def get_order(orderID):

    return

def get_order_by_user(userID):

    return

def add_agent_to_order():

    return

def update_orderTime(time,orderID):

    return

def update_readyTime(time,orderID):

    return

def update_acceptTime(time,orderID):

    return

def update_pickupTime(time,orderID):

    return

def update_deliveryTime(time,orderID):

    return

def update_confirmationTime(time,orderID):

    return
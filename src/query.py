#This document will contain all the queries to be used by the application

#Displays all menu types and location
def display_menu_type(cmd):
    result = menu.find({},{"type":1,"location":1})
    return

def display_order():
    result = order.find({},{})
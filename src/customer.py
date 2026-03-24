# Authors: Surya Balram

import notification     #importing member functions from notification.py
import order            #importing member functions from order.py
import menu             #importing member functions from menu.py

##Notification.py
#viewNotification



##order.py
#place_Order
def customer_place_order(self):
    bool message = place_Order(self)     #function to place an order

#viewOrder
def customer_view_order(self):
    dict message = viewOrder(self)       #function to view an order

#seeAllTimes = TBD

#addToCart = input
def customer_add_to_cart(self):
    menu_Item = input("Enter the menu item you want to add to your cart: ").strip()
    quantity = input("Enter the quantity: ").strip()
    add_to_cart(self, menu_Item, quantity)     #function to add items to cart

#viewCart
def customer_view_cart(self):
    dict message = view_cart(self)         #function to view the cart

#enterLocation = input




##menu.py
#viewMenu = input


#viewAllMenus
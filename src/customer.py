# Authors: Surya Balram

import notification     #importing member functions from notification.py
from order import Order,Cart            #importing member functions from order.py
from menu import Menu            #importing member functions from menu.py

## Notification.py
#viewNotification



## order.py
#place_order
def customer_place_order(self, order : Order):
    message : bool = order.place_order(self)    #calls place_order function from order.py and stores in message variable
    if message:
        print(f"\nOrder placed successfully! Order ID: {self.__order_id}")
        print(f"Delivering to: Building {self.__building}, Room {self.__room}")
        print(f"Subtotal: ${self.__subtotal:.2f}")		#print statements indicating important info
    else:
        print("Cannot place an order with no items.")


#view_order
def customer_view_order(self, order : Order):
    message : dict = order.view_order(self)      #calls view_order function from order.py and stores in message variable
    print("\n" + "─" * 50)							#divider
	print(f"  Order ID:      {self.__order_id or 'Not placed yet'}")			#orderID or message of unplaced order
	print(f"  Customer:      {self.__customer}")								#who be the customer
	print(f"  Vendor:        {self.__vendor}")									#who be the vendor
	print(f"  Agent:         {self.__agent or 'Unassigned'}")					#who be the agent, hUHHHHHH nobody?!?!?!
	print(f"  Location:      Building {self.__building}, Room {self.__room}")	#location be this
	print(f"  Subtotal:      ${self.__subtotal:.2f}")							#taxes may or may not be included
	print(f"  Status:        {self.__order_status}")							#THIS BE THE STATUS

    if message.get.__special_instructions:
        print(f"  Instructions:  {self.__special_instructions}")				#maybe it's special, maybe it's not
    if message.get.__placed_time:
		print(f"  Placed at:     {self.__placed_time.strftime('%Y-%m-%d %H:%M')}") #is it placed? or maybe it is not?!?!?!
	print("─" * 50)									#divider

#seeAllTimes / TBD

#addToCart = input
def customer_add_to_cart(self, order : Order):
    menu_item = input("Enter the menu item you want to add to your cart: ").strip()     #asks user to input the menu item, and stores in menu_Item variable
    quantity = input("Enter the quantity: ").strip()    #asks user to input the quantity, and stores in quantity variable
    add_to_cart(self, menu_item, quantity)              #passes menu_item and quantity to add_to_cart function from order.py

#view_cart
def customer_view_cart(self, order : Order):
    message : dict = order.view_cart(self)      #calls view_cart function from order.py and stores in message variable

    if not message.get.__cart_items:
        print("Your cart is empty.")				#calling this with an empty cart is dumb

    print(f"\n{'Item':<25} {'Qty':>5}")				#printing column with spacing and divider
	print("─" * 35)

    

#enterLocation = input / TBD



## menu.py
#viewMenu = input
def customer_view_menu(self, menu : Menu):
    keyword = input("Search keyword (leave blank for all): ").strip()   #asks user to input a search keyword, and stores in keyword variable
    menu.view_menu(self, keyword)            #passes keyword to view_menu function from menu.py

#viewAllMenus
def customer_view_all_menus(self):
    message = view_all_menus(self)      #calls view_all_menus function from menu.py and stores in message variable
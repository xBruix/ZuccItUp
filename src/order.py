# Authors: Caleb Bronn, Bruce Fernandes

from typing import Type	# supports using a class as an argument for a function
from enum import Enum	# for enumerations
from datetime import datetime
from server import Server


class Cart:
	def __init__(self, building: str, room: str):
		# You can declare private attributes using double underscores (__)
		# before the name of the variable
		self.__building = building
		self.__room = room
		self.__subtotal = 0.0

		# Format of cart items:
		# {
		#   "menuItemID": quantity (int),
		#   ...
		# }
		self.__cart_items = {}
#──────────────────────────────────────────────
# Getters
#──────────────────────────────────────────────
	def get_location(self) -> tuple:
		# Tuple data type in Python is an ordered, unchangeable array of data
		# See: https://www.w3schools.com/python/python_tuples.asp
		return self.__building, self.__room

	def get_subtotal(self) -> float:
		return self.__subtotal

	def get_cart_items(self) -> dict:
		return self.__cart_items

	# Setters
	def set_location(self, building: str, room: str):
		pass
#──────────────────────────────────────────────
# Other functions
#──────────────────────────────────────────────
	def add_to_cart(self, menu_item: str, quantity: int):

		if quantity <= 0:
			print("Quantity must be greater than 0.")	#avoiding troll inputs
			return

		"""
		result = list(db.menu.aggregate([				#checks for availability and existence of the item. using $match combines the check
			{"$unwind": "$menuItem"},					#unwinding the array of menuItem to separate menus
			{"$match": {
				"menuItem.name": {"$regex": f"^{menu_item}$", "$options": "i"},
				"menuItem.inStock": True
			}},
			{"$project": {"name": "$menuItem.name"}},
			{"$limit": 1}
		]))
		"""
		result = list(self.__server.get_menu_item(menu_item))	#calling server
  
		if not result or not result[0].get("inStock"):
			print(f"'{menu_item}' is out of stock.")	#if it is not available it gives this message
			return

		canonical_name = result[0]["name"]				#the true name as given in the database(Chicken Strips and not chicken sTRIps)

		if canonical_name in self.__cart_items:			#this checks if the item is already in the cart, if so it just adds to the quantity of the item
			self.__cart_items[canonical_name] += quantity

		else:
			self.__cart_items[canonical_name] = quantity
		print(f"Added {quantity}x '{canonical_name}' to cart.")

	def change_quantity(self, menu_item: str, quantity: int):
     
		if menu_item not in self.__cart_items:			#cannot change the quantity if it isn't in the cart
			print(f"'{menu_item}' is not in the cart.")
			return

		if quantity <= 0:								#if the new quantity is 0 or negative, assume it is calling for removal
			self.remove_from_cart(menu_item)

		else:
			self.__cart_items[menu_item] = quantity		#updating the quantity to the new quantity given, if it is meant to be incremental or decremental please change this
			print(f"Updated '{menu_item}' quantity to {quantity}.")

	def remove_from_cart(self, menu_item: str):
     
		if menu_item in self.__cart_items:
			del self.__cart_items[menu_item]
			print(f"Removed '{menu_item}' from cart.")	#simply removing the item chosen
   
		else:
			print(f"'{menu_item}' is not in the cart.")	#if they try to break the program by removing something that is not there, this checks for that

	def calculate_subtotal(self) -> float:
		total = 0.0
		"""
		for item_name, qty in self.__cart_items.items():#looping through every item in the cart, giving item name and quantity
			result = list(db.menu.aggregate([			
            {"$unwind": "$menuItem"},
            {"$match": {"menuItem.name": {"$regex": f"^{item_name}$", "$options": "i"}}},
            {"$project": {"price": "$menuItem.price"}},
            {"$limit": 1}								#for each item we check price
        ]))
		"""
		for item_name, qty in self.__cart_item.items():	#looping through every item in the cart, giving item name and quantity
      
			result = list(self.__server.get_menu_item(item_name))	#for each item we check price
	
			if result:									#adding price accounting for the quantity
				total += result[0]["price"] * qty	
			
			else:										#sanity check if price is not in the menu
				print(f"Warning: price for '{item_name}' not found in menu.")
            
		self.__subtotal = round(total, 2)
		return self.__subtotal							#rounding the total and returning it so its a dollar amount $42.069 as a total does not make sense

	def view_cart(self) -> dict:

		if not self.__cart_items:
			print("Your cart is empty.")				#calling this with an empty cart is dumb
			return {}

		print(f"\n{'Item':<25} {'Qty':>5}")				#printing column with spacing and divider
		print("─" * 35)

		for item, qty in self.__cart_items.items():		#looping through to print each item and quantity aligned with the column made above
			print(f"{item:<25} {qty:>5}")
   
		print("─" * 35)									#closing divider line
		print(f"Delivery to: Building {self.__building}, Room {self.__room}")
		return self.__cart_items						#prints delivery location and returns the dictionary

	def num_items(self) -> int:
		return len(self.__cart_items)					#!!!!!!!!!!!!!!!!Bruce did not write this, please comment this!!!!!!!!!!!!!

	def convert_to_orders(self):

		if not self.__cart_items:
			print("Cannot place an empty order.")		#again, calling this with an empty cart means you need to seek psyciatric help(i cannot spell)
			return None

		subtotal = self.calculate_subtotal()			#calling the subtotal function to display the subtotal as required

		order = Order(									#creating the order(i might be missing something here)
			building=self.__building,
			room=self.__room,
			total=subtotal,
			customer=customer,
			vendor=vendor,
			server=self.__server,
		)
  
		self.__cart_items = {}							#clearing the cart for the next order after making it into an order
		self.__subtotal = 0.0
  
		return order									#returning the order does not mean the order is placed, place_order() should be called i think
		


#──────────────────────────────────────────────
# End of Cart
#──────────────────────────────────────────────

#──────────────────────────────────────────────
# Short enum class for order times:
#──────────────────────────────────────────────
class Time(Enum):
	ORDER = "Order"
	READY = "Ready"
	ACCEPT = "Accept"
	PICKUP = "Pickup"
	DELIVERY = "Delivery"
	CONFIRMATION = "Confirmation"
#──────────────────────────────────────────────
# End of Time class
#──────────────────────────────────────────────


#──────────────────────────────────────────────
# Short enum class for order status:
#──────────────────────────────────────────────
class Status(Enum):
	# Not quite sure how to do this, but here's some ideas:
	PENDING = "Pending"	# waiting for agent to accept the order
	READY_FOR_PICKUP = "ReadyForPickup"
	IN_TRANSIT = "InTransit"
	DELIVERED = "Delivered"
	RECEIVED = "Received"
#──────────────────────────────────────────────
# End of Status class
#──────────────────────────────────────────────


class Order:
	def __init__(self, svr: Server, building: str, room: str, total: float, instructions: str, customer: str, vendor: str):
		self.__server = svr
		self.__building = building
		self.__room = room
		self.__subtotal = total
		self.__special_instructions = instructions
		self.__customer = customer
		self.__vendor = vendor
		self.__agent = ""
		self.__order_id = ""
		self.__order_status = ""
		self.__order_time = ""
		self.__ready_time = ""
		self.__accept_time = ""
		self.__pickup_time = ""
		self.__delivery_time = ""
		self.__confirmation_time = ""
#──────────────────────────────────────────────
# Getters
#──────────────────────────────────────────────
	def get_location(self) -> tuple:
		return self.__building, self.__room

	def get_subtotal(self) -> float:
		return self.__subtotal

	def get_instructions(self) -> str:
		return self.__special_instructions

	def get_status(self) -> str:
		return self.__order_status

	def get_time(self, time_enum: Type[Time]) -> str:
		if time_enum == Time.ORDER:
			return self.__order_time
		elif time_enum == Time.READY:
			return self.__ready_time
		elif time_enum == Time.ACCEPT:
			return self.__accept_time
		elif time_enum == Time.PICKUP:
			return self.__pickup_time
		elif time_enum == Time.DELIVERY:
			return self.__delivery_time
		elif time_enum == Time.CONFIRMATION:
			return self.__confirmation_time
		else:
			raise ValueError("Unknown time ENUM")
#──────────────────────────────────────────────
# Setters
#──────────────────────────────────────────────
	def set_instructions(self, instructions: str):
		self.__special_instructions = instructions

#──────────────────────────────────────────────
# Other functions
#──────────────────────────────────────────────

	#I HAVE JUST UPDATED THIS ENTIRE THING TO WORK WITH SERVER.PY
	def update_status(self, status: Type[Status]):		#with this we assume status is the status we want to change the order to
		self.__order_status = status.value				#extracting the string
		now = datetime.now()							#capturing the current date and time for later use


		if status == Status.READY_FOR_PICKUP:
			self.__ready_time = now	
			if self.__order_id:
				self.__server.update_order_status(self.__order_id, self.__order_status)
				self.__server.update_readyTime(now, self.__order_id)

		elif status == Status.IN_TRANSIT:
			self.__pickup_time = now
			if self.__order_id:
				self.__server.update_order_status(self.__order_id, self.__order_status)
				self.__server.update_pickupTime(now, self.__order_id)
    
		elif status == Status.DELIVERED:
			self.__delivery_time = now
			if self.__order_id:
				self.__server.update_order_status(self.__order_id, self.__order_status)
				self.__server.update_deliveryTime(now, self.__order_id)
    
		elif status == Status.RECEIVED:
			self.__confirmation_time = now
			if self.__order_id:
				self.__server.update_order_status(self.__order_id, self.__order_status)
				self.__server.update_confirmationTime(now, self.__order_id)
    
		elif self.__order_id:
			#Fallback: just update the status field for any other status. this is just a failsafe
			self.__server.update_order_status(self.__order_id, self.__order_status)

		print(f"Order status updated to: {status.value}") #prints the change to the user, will omit this later since the user does not actually need this unless they ask for it

	def place_order(self) -> bool:
     
		if not self.__cart_items:
			print("Cannot place an order with no items.")
			return False								#sanity check for morons that want to order "nothing"

		self.__order_time = datetime.now()				#recording order time
		self.__order_status = Status.PENDING.value		#setting initial status
  
		sanitized_items = [
			{"name": item["name"], "qty": int(item["qty"])}
			for name, qty in self.__cart_items.items()	#List to rebuild each cart item, casting quantity as int because when i googled, mangodb messes with floats and stuff
		]

		#changed this to call server.py for the insertion
		self.__order_id = self.__server.create_order(
			building=self.__building,
			room=self.__room,
			subtotal=float(self.__subtotal),
			instructions=self.__special_instructions,
			customer=self.__customer,
			vendor=self.__vendor,
			cart=sanitized_items,
		)				

		"""
		result = db.order.insert_one(order_doc)			#insering the document into the collection. mango should respond with an object containing the new document's ID
		self.__order_id = result.inserted_id			#saving the ID onto the object which all the order methods will use to find the particular order

		
		print(f"\nOrder placed successfully! Order ID: {self.__order_id}")
		print(f"Delivering to: Building {self.__building}, Room {self.__room}")
		print(f"Subtotal: ${self.__subtotal:.2f}")		#print statements indicating important info
		"""
		self.__server.update_orderTime(self.__order_time, self.__order_id)
  
		return True										#returns success to the caller

	def accept_order(self, agent: str):
     
		if not self.__order_id:
			print("Order has not been placed yet.")
			return										#how is man going to acccept an order that isn't placed(just a check so things don't break)

		self.__agent = agent							#assigning agent
		self.__accept_time = datetime.now()				#marking the time the order is accepted
		self.__order_status = Status.IN_TRANSIT.value	#changing order status for obvious reasons

		self.__server.add_agent_to_order(order_id=self.__order_id, agent_id=self.__agent)
		self.__server.update_order_status(order_id=self.__order_id, status=self.__order_status)
		self.__server.update_acceptTime(time=self.__accept_time, order_id=self.__order_id)
  
		print(f"Order accepted by agent '{agent}'.")	#saying who actually accepted the order

	def mark_complete(self):
     
		if not self.__order_id:
			print("Order has not been placed yet.")
			return										#yet another check for the system not to break completely

		self.__delivery_time = datetime.now()			#marking delivery time
		self.__order_status = Status.DELIVERED.value		#updaing the orderStatus
		self.__server.update_order_status(order_id=self.__order_id, status=self.__order_status)
		self.__server.update_orderTime(time=self.__delivery_time, order_id=self.__order_id)
  
		print("Order marked as complete.")				#messaging that the order is complete

	def view_order(self) -> dict:
		order_dict = {
			"order_id": str(self.__order_id) if self.__order_id else None,
			"customer": self.__customer,
			"vendor": self.__vendor,
			"agent": self.__agent,
			"building": self.__building,
			"room": self.__room,
			"subtotal": self.__subtotal,
			"status": self.__order_status,
			"special_instructions": self.__special_instructions,
			"order_time": self.__order_time,
			"accept_time": self.__accept_time,
			"ready_time": self.__ready_time,
			"pickup_time": self.__pickup_time,
			"delivery_time": self.__delivery_time,
			"confirmation_time": self.__confirmation_time,
		}												#i hate my life, i think this is the entire thing(building the dictionary)

		print("\n" + "─" * 50)							#divider
		print(f"  Order ID:      {self.__order_id or 'Not placed yet'}")			#orderID or message of unplaced order
		print(f"  Customer:      {self.__customer}")								#who be the customer
		print(f"  Vendor:        {self.__vendor}")									#who be the vendor
		print(f"  Agent:         {self.__agent or 'Unassigned'}")					#who be the agent, hUHHHHHH nobody?!?!?!
		print(f"  Location:      Building {self.__building}, Room {self.__room}")	#location be this
		print(f"  Subtotal:      ${self.__subtotal:.2f}")							#taxes may or may not be included
		print(f"  Status:        {self.__order_status}")							#THIS BE THE STATUS
		if self.__special_instructions:
			print(f"  Instructions:  {self.__special_instructions}")				#maybe it's special, maybe it's not
		if self.__order_time:
			print(f"  Placed at:     {self.__order_time.strftime('%Y-%m-%d %H:%M')}") #is it placed? or maybe it is not?!?!?!
		print("─" * 50)									#divider
		return order_dict								#i have lost my mind

	def view_all_orders(self) -> list[dict]:
		
		#changed this to call server.py
		orders = self.__server.get_all_orders()
  
		if not orders:
			print("No orders found.")
			return []									#this is cwaaaaazy, no orders at all?????????

		print(f"\n{'Customer':<15} {'Vendor':<15} {'Status':<18} {'Subtotal':>10}  Location")
		print("─" * 80)									#table spacing and divider
		for o in orders:
			loc = f"Bldg {o.get('building')}, Rm {o.get('room')}"	#this is my way of fixing if the string ever gets too long
			print(
				f"{o.get('customer', ''):<15} "
				f"{o.get('vendor', ''):<15} "
				f"{o.get('orderStatus', ''):<18} "
				f"${o.get('subTotal', 0.0):>9.2f}  "	#this one has the 0.0 so if the subtotal is missing, it does not break and print junk values
				f"{loc}"
			)
		return orders									#we made it to the end yay
#──────────────────────────────────────────────
# End of Order
#──────────────────────────────────────────────
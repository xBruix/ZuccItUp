# Authors: Caleb Bronn, Bruce also did the cart functions and is going to do the later order functions

from typing import Type	# supports using a class as an argument for a function
from enum import Enum	# for enumerations


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

		result = list(db.menu.aggregate([				#checks for availability and existence of the item. using $match combines the check
			{"$unwind": "$menuItem"},					#unwinding the array of menuItem to separate menus
			{"$match": {
				"menuItem.name": {"$regex": f"^{menu_item}$", "$options": "i"},
				"menuItem.inStock": True
			}},
			{"$project": {"name": "$menuItem.name"}},
			{"$limit": 1}
		]))

		if not result:
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
  
		for item_name, qty in self.__cart_items.items():#looping through every item in the cart, giving item name and quantity
			result = list(db.menu.aggregate([			
            {"$unwind": "$menuItem"},
            {"$match": {"menuItem.name": {"$regex": f"^{item_name}$", "$options": "i"}}},
            {"$project": {"price": "$menuItem.price"}},
            {"$limit": 1}								#for each item we check price
        ]))
   
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
	ORDER = "ORDER"
	READY = "READY"
	ACCEPT = "ACCEPT"
	PICKUP = "PICKUP"
	DELIVERY = "DELIVERY"
	CONFIRMATION = "CONFIRMATION"
#──────────────────────────────────────────────
# End of Time class
#──────────────────────────────────────────────


#──────────────────────────────────────────────
# Short enum class for order status:
#──────────────────────────────────────────────
class Status(Enum):
	# Not quite sure how to do this, but here's some ideas:
	# PENDING = "PENDING"	# waiting for agent to accept the order
	# READY_FOR_PICKUP = "READY_FOR_PICKUP"
	# IN_TRANSIT = "IN_TRANSIT"
	# DELIVERED = "DELIVERED"
	# RECEIVED = "RECEIVED"
	pass
#──────────────────────────────────────────────
# End of Status class
#──────────────────────────────────────────────


class Order:
	def __init__(self, building: str, room: str, total: float, instructions: str, customer: str, vendor: str):
		self.__building = building
		self.__room = room
		self.__subtotal = total
		self.__special_instructions = instructions
		self.__customer = customer
		self.__vendor = vendor
		self.__agent = ""
		self.__order_id = ""
		self.__order_status = ""
		self.__placed_time = ""
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
		if time_enum == Time.PLACED:
			return self.__placed_time
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
	def update_status(self, status: Type[Status]):
		self.__order_status = status.value
		now = datetime.now()

		update_fields = {"orderStatus": self.__order_status}

		if status == Status.READY_FOR_PICKUP:
			self.__ready_time = now
			update_fields["readyTime"] = now

		elif status == Status.IN_TRANSIT:
			self.__pickup_time = now
			update_fields["pickupTime"] = now

		elif status == Status.DELIVERED:
			self.__delivery_time = now
			update_fields["deliveryTime"] = now

		elif status == Status.RECEIVED:
			self.__confirmation_time = now
			update_fields["acceptTime"] = now

		if self.__order_id:
			db.order.update_one(
				{"_id": self.__order_id},
				{"$set": update_fields}
			)

		print(f"Order status updated to: {status.value}")

	def place_order(self) -> bool:
     
		if not cart_items:
			print("Cannot place an order with no items.")
			return False

		self.__placed_time = datetime.now()

		sanitized_items = [
			{"name": item["name"], "qty": int(item["qty"])}
			for item in cart_items
		]

		order_doc = {
			"building": self.__building,
			"room": self.__room,
			"subTotal": float(self.__subtotal),
			"specialInstructions": self.__special_instructions,
			"orderStatus": self.__order_status,
			"orderTime": self.__placed_time,
			"readyTime": None,
			"acceptTime": None,
			"pickupTime": None,
			"deliveryTime": None,
			"agent": self.__agent,
			"customer": self.__customer,
			"vendor": self.__vendor,
			"cartItem": sanitized_items,
		}

		result = db.order.insert_one(order_doc)
		self.__order_id = result.inserted_id
		print(f"\nOrder placed successfully! Order ID: {self.__order_id}")
		print(f"Delivering to: Building {self.__building}, Room {self.__room}")
		print(f"Subtotal: ${self.__subtotal:.2f}")
		return True

	def accept_order(self, agent: str):
     
		if not self.__order_id:
			print("Order has not been placed yet.")
			return

		self.__agent = agent
		self.__accept_time = datetime.now()
		self.__order_status = Status.IN_TRANSIT.value

		db.order.update_one(
			{"_id": self.__order_id},
			{"$set": {
				"agent": agent,
				"orderStatus": self.__order_status,
				"acceptTime": self.__accept_time,
			}}
		)
		print(f"Order accepted by agent '{agent}'.")

	def mark_complete(self):
		pass

	def view_order(self) -> dict:
		pass

	def view_all_orders(self) -> list[dict]:
		orders = list(db.order.find())
		if not orders:
			print("No orders found.")
			return []

		print(f"\n{'Customer':<15} {'Vendor':<15} {'Status':<18} {'Subtotal':>10}  Location")
		print("─" * 80)
		for o in orders:
			loc = f"Bldg {o.get('building')}, Rm {o.get('room')}"
			print(
				f"{o.get('customer', ''):<15} "
				f"{o.get('vendor', ''):<15} "
				f"{o.get('orderStatus', ''):<18} "
				f"${o.get('subTotal', 0.0):>9.2f}  "
				f"{loc}"
			)
		return orders
#──────────────────────────────────────────────
# End of Order
#──────────────────────────────────────────────
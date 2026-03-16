# Authors: Caleb Bronn

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

	# Getters
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

	# Other functions
	def add_to_cart(self, menu_item: str, quantity: int):
		pass

	def change_quantity(self, menu_item: str, quantity: int):
		pass

	def remove_from_cart(self, menu_item: str):
		pass

	def calculate_subtotal(self) -> float:
		pass

	def view_cart(self) -> dict:
		pass

	def num_items(self) -> int:
		return len(self.__cart_items)

	def convert_to_orders(self):
		pass
# End of Cart


# Short enum class for order times:
class Time(Enum):
	PLACED = "PLACED"
	READY = "READY"
	ACCEPT = "ACCEPT"
	PICKUP = "PICKUP"
	DELIVERY = "DELIVERY"
	CONFIRMATION = "CONFIRMATION"
# End of Time class


# Short enum class for order status:
class Status(Enum):
	# Not quite sure how to do this, but here's some ideas:
	# WAITING = "WAITING"	# waiting for agent to accept the order
	# READY_FOR_PICKUP = "READY_FOR_PICKUP"
	# IN_TRANSIT = "IN_TRANSIT"
	# DELIVERED = "DELIVERED"
	# RECEIVED = "RECEIVED"
	pass
# End of Status class


class Order:
	def __init__(self, building: str,
				 room: str,
				 total: float,
				 instructions: str,
				 customer: str,
				 vendor: str
				 ):
		self.__building = building
		self.__room = room
		self.__total = total
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

	# Getters
	def get_location(self) -> tuple:
		return self.__building, self.__room

	def get_total(self) -> float:
		return self.__total

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

	# Setters
	def set_instructions(self, instructions: str):
		self.__special_instructions = instructions

	# Other functions
	def update_status(self, status: Type[Status]):
		pass

	def place_order(self) -> bool:
		pass

	def accept_order(self, agent: str):
		pass

	def mark_complete(self):
		pass

	def view_order(self) -> dict:
		pass

	def view_all_orders(self) -> list[dict]:
		pass
# End of Order
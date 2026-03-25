# Authors: Caleb, Keenan
from datetime import datetime
from pymongo import MongoClient as MangoClient
from bson.objectid import ObjectId

#See code plan in A6 document for details on each function


class Server:
	"""
	Creates the MangoDB client, connects to the database, and gets the collections.
	This then allows other code to interact with the database and get back data as Python
	data types.

	Parameters:
	:param str user_id: the user's MongoDB username
	:param str passwd: the user's MongoDB password
	"""
	def __init__(self, user_id: str, passwd: str):
		# DEBUG
		# print("Username: " + user_id)
		# print("Password: " + passwd)

		# Name of the project you want to connect to, e.g. csci375a_project
		self.__project = user_id + "_project"

		# URI of the MangoDB server
		self.__uri = f"mongodb://{user_id}:{passwd}@studb-mongo.csci.viu.ca:27017/{self.__project}?authSource=admin"

		# Create DB Client or throw an exception if the user ID or password is incorrect.
		try:
			self.__client = MangoClient(self.__uri)
			self.__db = self.__client.get_database(self.__project)
			# Ping the database to check that username and password are actually correct
			self.__db.command("ping")
		except Exception:
			# Username and/or password were NOT correct
			raise ValueError("Could not connect to MongoDB: username or password was incorrect")
		else:
			# Get collections as private attributes
			self.__user = self.__db["user"]
			self.__menu = self.__db["menu"]
			self.__order = self.__db["order"]
	# end __init__

	# User functions

	def disconnect(self):
		"""Severs the connection to the database server"""
		self.__client.close()

	def verify_user(self, viu_id: str) -> bool:
		result = self.__user.find_one({
			"VIUID": viu_id
		})
		return result is not None

	def create_user(self, email: str, name: str, viu_id: str, role: str, availability_status: bool = None):
		"""
		Inserts a new user to the user collection. If the user already exists, it sets their status to active.
		Parameters:
		:param email: A valid email address
		:param name: The user's name
		:param viu_id: The user's VIU ID number (9 digits)
		:param role: Must be either 'customer' or 'agent'
		:param availability_status: Optional, true for available, false for unavailable

		Exceptions:
		:raises ValueError: If an invalid parameter is given. A parameter is invalid if it doesn't align
		with the criteria in DB_validation.py
		"""
		if self.verify_user(viu_id):
			self.__user.update_one(
				{"VIUID": viu_id},
				{"$set": {"active": True}}
			)

		new_user_doc = {
			"name": name,
			"email": email,
			"VIUID": viu_id,
			"role": role.title(),	# Ensures that the role is capitalized
			"active": True,
			"previouslyOrdered": []
		}

		if availability_status is not None:
			new_user_doc["availabilityStatus"] = availability_status

		try:
			self.__user.insert_one(new_user_doc)
		except Exception:
			raise ValueError("Invalid parameter in create_user. Ensure that parameters follow the criteria given in DB_validation.py")

	def deactivate_user(self, viu_id: str):
		self.__user.update_one(
			{"VIUID": viu_id},
			{"$set":
				 {"active": False}
			}
		)

	def view_all_users(self, role: str) -> list[dict]:
		results = self.__user.find({"role": role})
		return results.to_list()

	def view_user(self, viu_id: str) -> dict:
		return self.__user.find_one({"VIUID": viu_id})


	# Menu functions

	#gets all vendor names

	# NOTE: we don't need get_vendors since you could just call view_all_users("Vendor") to do the same thing
	def get_vendors(self) -> list[dict]:
		result = self.__menu.distinct("vendor")

		""" for vendor in result
			print(f" - {vendor}")   #print example for distinct vendors that have menus 
		"""
		return result

	# whichever param is filled will change the query,
	# if vendor_id=upper cafe it will display upper cafe menus
	# if menuItem = coffee it will find menu with coffee
	# null of all should return all menus
	def get_all_menus(self, vendor_id: str=None, menu_item: str=None, menu_type: str=None) -> list[dict]:
		query = {}

		if vendor_id:
			query["vendor"] = vendor_id

		if menu_item:
			query["menuItem"] = menu_item

		if menu_type:
			query["type"] = menu_type.title()	# Capitalizes the string

		result = self.__menu.find(query)
		return result.to_list()

	#by type and/or by vendor
	# both params are used it will display the menu with both conditions
	def get_one_menu(self, vendor_name: str, menu_type: str) -> dict:
		query = {
			"vendor": vendor_name,
			"type": menu_type.title()
		}
		return self.__menu.find_one(query)

	#used by view Item or view all items
	# with param means display one menu item
	# with param = null display all menus
	def get_menu_item(self, menu_item_id: str = None) -> dict:

		if menu_item_id:
			result = self.__menu.aggregate([                    #runs aggregation pipeline against menu collection and converts it into a list
				{"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
				{"$match": {"menuItem.name": {"$regex": menu_item_id, "$options": "i"}}}, #filters to where only the matching item remains
				{"$project": {                                   #selects only the fields required and ignores the rest
					"name": "$menuItem.name",
					"price": "$menuItem.price",
					"description": "$menuItem.description",
					"inStock": "$menuItem.inStock",
					"allergens": "$menuItem.allergens",          #from "name" till this line, pulls fields from the unwound menuItem and allows acess as just item["name"]
					"location": "$location",
					"menuType": "$type",                         #these two lines pull fields from the menu document to find location and menuType the item belongs
				}},
				{"$limit": 1}
			])
			return result

		result = self.__menu.aggregate([                     #runs the aggregation pipeline on the menu collection and converts it to the python list
				{"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
				{"$project": {                                   #selects the fields we want to output
					"name": "$menuItem.name",
					"price": "$menuItem.price",
					"description": "$menuItem.description",
					"inStock": "$menuItem.inStock",              #pulls the four fields from the unwound menuItem in the form item["name"], item["price"] and such
					"location": "$location",
					"menuType": "$type",                         #pulling these two fields from the menu document to find the location and menuType for each item
				}},
				{"$sort": {"location": 1, "menuType": 1, "name": 1}} #sorts the results by location, then menuType and then name alphabetically, grouping the output logically by place, type and such
			])

		return result

	# Order functions

	# for order identification we are using the given _id from mongodb
	def create_order(self, building: str, room: str, subtotal: float, instructions: str, customer: str, vendor: str, cart: list[dict]) -> str:
		order_doc = {
			"building": building,
			"room": room,
			"subTotal": subtotal,
			"specialInstructions": instructions,
			"customer": customer,
			"vendor": vendor.title(),	# Make sure vendor name is capitalized properly
			"cartItem": cart,
			"orderStatus": "Pending",
			"orderTime": datetime.now()
		}

		result = self.__order.insert_one(order_doc)
		return str(result.inserted_id)


	def get_order_by_id(self, order_id: str) -> dict:
		result = self.__order.find_one({"_id": ObjectId(order_id)})
		return result


	def get_orders_by_user(self, user_id: str) -> list[dict]:
		result = self.__order.find({
			"$or": [
				{"customer": user_id},
				{"agent": user_id}
			]
		})
		return result.to_list()


	def add_agent_to_order(self, order_id: str, agent_id: str) -> int:
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"agent": agent_id}}
		)
		return result.modified_count


	def update_orderTime(self, time: datetime, order_id: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"orderTime": time}}
		)
		return result.modified_count


	def update_readyTime(self, time: datetime, order_id: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"readyTime": time}}
		)
		return result.modified_count


	def update_acceptTime(self, time: datetime, order_id: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"acceptTime": time}}
		)
		return result.modified_count


	def update_pickupTime(self, time: datetime, order_id: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"pickupTime": time}}
		)
		return result.modified_count


	def update_deliveryTime(self, time: datetime, order_id: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"deliveryTime": time}}
		)
		return result.modified_count


	def update_confirmationTime(self, time: datetime, order_id: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"confirmationTime": time}}
		)
		return result.modified_count

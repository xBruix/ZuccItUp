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
	:param str user_ID: the user's MongoDB username
	:param str passwd: the user's MongoDB password
	"""
	def __init__(self, user_ID: str, passwd: str):
		# DEBUG
		# print("Username: " + user_ID)
		# print("Password: " + passwd)

		# Name of the project you want to connect to, e.g. csci375a_project
		self.__project = user_ID + "_project"

		# URI of the MangoDB server
		self.__uri = f"mongodb://{user_ID}:{passwd}@studb-mongo.csci.viu.ca:27017/{self.__project}?authSource=admin"

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

	def verify_user(self, viu_ID: str) -> bool:
		result = self.__user.find_one({
			"VIUID": viu_ID
		})
		return result is not None

	def create_user(self, email: str, name: str, viu_ID: str, role: str, availability_status: bool=None) -> str:
		"""
		Inserts a new user to the user collection.
		Parameters:
		:param email: A valid email address
		:param name: The user's name
		:param viu_ID: The user's VIU ID number (9 digits)
		:param role: Must be either 'customer' or 'agent'
		:param availability_status: Optional, true for available, false for unavailable
		Returns:
		:return str: the newly-created user's MongoDB ID number
		Exceptions:
		:raises ValueError: if the user already exists
		"""
		if self.verify_user(viu_ID):
			raise ValueError("User already exists")

		if role.lower() == "agent":
			agent_doc = {
				"name": name,
				"email": email,
				"VIUID": viu_ID,
				"role": role,
				"active": True,
				"availabilityStatus": availability_status	# defining the agent to be added to the db with the required details
			}
			result = self.__user.insert_one(agent_doc)
			return str(result.inserted_id)

		elif role.lower() == "customer":
			customer_doc = {
				"name": name,
				"email": email,
				"VIUID": viu_ID,
				"role": role,
				"active": True,
				"previouslyOrdered": []
			}
			result = self.__user.insert_one(customer_doc)
			return str(result.inserted_id)

	def deactivate_user(self, viu_ID: str):
		self.__user.update_one(
			{"VIUID": viu_ID},
			{"$set":
				 {"active": False}
			}
		)

	def view_all_users(self, role: str) -> list[dict]:
		results = self.__user.find({"role": role})
		return results.to_list()

	def view_user(self, viu_ID: str) -> dict:
		return self.__user.find_one({"VIUID": viu_ID})


	# Menu functions

	#gets all vendor names
	def get_vendors(self) -> list[dict]:
		result = self.__menu.distinct("vendor")

		""" for vendor in result
			print(f" - {vendor}")   #print example for distinct vendors that have menus 
		"""
		return result

	# whichever param is filled will change the query,
	# if vendor_ID=upper cafe it will display upper cafe menus
	# if menuItem = coffee it will find menu with coffee
	# null of all should return all menus
	def get_all_menus(self, vendor_ID: str=None, menu_item: str=None, menu_type: str=None) -> list[dict]:
		query = {}

		if vendor_ID:
			query["vendor"] = vendor_ID

		if menu_item:
			query["menuItem"] = menu_item

		if menu_type:
			query["type"] = menu_type.title()	# Capitalizes the string

		result = self.__menu.find(query)
		return result.to_list()

	#by type and/or by vendor
	# both params are used it will display the menu with both conditions
	# works with only one param but will still only display one menu
	def get_one_menu(self, vendor_ID: str=None, menu_type: str=None) -> dict:
		query = {}

		if vendor_ID:
			query["vendor"] = vendor_ID

		if menu_type:
			query["type"] = menu_type.title()

		result = self.__menu.find_one(query)

		return result

	#used by view Item or view all items
	# with param means display one menu item
	# with param = null display all menus
	def get_menu_item(self, menu_item_ID=None) -> dict:

		if menu_item_ID:
			result = self.__menu.aggregate([                    #runs aggregation pipeline against menu collection and converts it into a list
				{"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
				{"$match": {"menuItem.name": {"$regex": menu_item_ID, "$options": "i"}}}, #filters to where only the matching item remains
				{"$project": {                                   #selects only the fields required and deletes the rest
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

	#order functions
	# for order identification we are using the given _id from mongodb
	def create_order(self, building: str, room: str, subtotal: float, instructions: str, customer: str, vendor: str, cart: list[dict]):
		order_doc = {
			"building": building,
			"room": room,
			"subTotal": subtotal,
			"specialInstructions": instructions,
			"customer": customer,
			"vendor": vendor,
			"cartItem": cart,
			"orderStatus": "Pending",
			"orderTime": datetime.now().strftime("%H%M")	# I think this should be just datetime.now()?
		}

		result = self.__order.insert_one(order_doc)
		return result.inserted_id


	def get_order(self, order_ID: str) -> dict:
		result = self.__order.find_one({"_id": ObjectId(order_ID)})
		return result


	def get_order_by_user(self, user_ID: str) -> list[dict]:
		result = self.__order.find({"customer": user_ID})
		return result.to_list()


	def add_agent_to_order(self, order_ID: str, agent_name: str) -> int:
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"agent": agent_name}}
		)
		return result.modified_count


	def update_orderTime(self, time: datetime, order_ID: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"orderTime": time}}
		)
		return result.modified_count


	def update_readyTime(self, time: datetime, order_ID: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"readyTime": time}}
		)
		return result.modified_count


	def update_acceptTime(self, time: datetime, order_ID: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"acceptTime": time}}
		)
		return result.modified_count


	def update_pickupTime(self, time: datetime, order_ID: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"pickupTime": time}}
		)
		return result.modified_count


	def update_deliveryTime(self, time: datetime, order_ID: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"deliveryTime": time}}
		)
		return result.modified_count


	def update_confirmationTime(self, time: datetime, order_ID: str):
		result = self.__order.update_one(
			{"_id": ObjectId(order_ID)},
			{"$set": {"confirmationTime": time}}
		)
		return result.modified_count

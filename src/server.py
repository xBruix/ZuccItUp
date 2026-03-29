# Authors: Caleb, Keenan
from datetime import datetime						# for handling times and dates
from pymongo import MongoClient as MangoClient		# MangoDB Client
from bson.objectid import ObjectId					# for MangoDB _id
import bcrypt										# for hashing and salting passwords

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

	# Two private helper functions for hashing and salting passwords
	# Here's where I got the code: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
	#
	# The .encode() method converts a string into a literal byte sequence, which is the data type that bcrypt uses.
	# Explanation here: https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
	def __generate_hashed_password(self, plaintext_passwd: str) -> str:
		return bcrypt.hashpw(plaintext_passwd.encode('UTF-8'), bcrypt.gensalt(12)).decode('UTF-8')

	def __check_hashed_password(self, plaintext_passwd: str, ciphertext_password: str) -> bool:
		return bcrypt.checkpw(plaintext_passwd.encode('UTF-8'), ciphertext_password.encode('UTF-8'))

	def verify_user(self, viu_id: str, passwd: str) -> bool:
		"""
		Verifies that the user exists. This is the same as logging in.
		:param viu_id: User's VIU ID number
		:param passwd: User's password
		:return: True if user is in DB, false if not
		"""
		result = self.__user.find_one({
			"VIUID": viu_id,
		})
		if result is None:
			return False
		else:
			# False if password doesn't match or user is deactivated, True otherwise
			return self.__check_hashed_password(passwd, result["password"]) and result["active"]

	def create_user(self, viu_id: str, passwd: str, email: str, name: str,  role: str, availability_status: bool = None):
		"""
		Inserts a new user to the user collection. If the user already exists, it sets their status to active.
		Parameters:
		:param viu_id: The user's VIU ID number (9 digits)
		:param passwd: The plaintext password entered by the user
		:param email: A valid email address
		:param name: The user's name
		:param role: Must be either 'customer' or 'agent'
		:param availability_status: Optional, true for available, false for unavailable

		Exceptions:
		:raises ValueError: If an invalid parameter is given. A parameter is invalid if it doesn't align
		with the criteria in DB_validation.py
		"""
		if self.verify_user(viu_id, passwd):
			self.__user.update_one(
				{"VIUID": viu_id},
				{"$set": {
					"active": True,
					"password": self.__generate_hashed_password(passwd)
					}
				}
			)

		new_user_doc = {
			"name": name,
			"email": email,
			"VIUID": viu_id,
			"password": self.__generate_hashed_password(passwd),
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
		"""
		Find user by ID and set status to false.
		:param viu_id: User's VIU ID number
		:raises ValueError: If an invalid VIU ID is given
		"""
		result = self.__user.update_one(
			{"VIUID": viu_id},
			{"$set": {
				"active": False,
				"previouslyOrdered": []
				}
			}
		)
		if result.matched_count == 0:
			raise ValueError("Invalid VIU ID in deactivate_user()")

	def view_all_users(self, role: str) -> list[dict]:
		"""
		Get a list of all users matching a particular role and returns their info.
		:param role: 'Agent' or 'Customer'
		:return: All info about users of the given role (except password)
		"""
		results = self.__user.find({"role": role}, {"password": 0})		# Don't include password in return value
		return results.to_list()

	def view_user(self, viu_id: str) -> dict:
		"""
		Find user by their ID and return all info about that user as a Python dictionary.
		:param viu_id: User's VIU ID number
		:return: a dictionary containing all user info (except password)
		"""
		return self.__user.find_one({"VIUID": viu_id}, {"password": 0})		# Don't include password in return value

	def update_availability(self, viu_ID: str, status: bool) -> int:
		"""
		Set an Agent's status
		:param viu_ID: User's VIU ID number
		:param status: The new availabilityStatus
		:return: 1 if status was changed, 0 if not
		"""
		result = self.__user.update_one(	
			{"VIUID": viu_ID, "role": "Agent"},
			{"$set": {"availabilityStatus": status}}	#updates if the agent with this viuid exists
		)
		return result.modified_count					#retuns 1 if changed, 0 if not
  
	# Menu functions

	def get_all_menus(self, vendor_name: str=None, item_name: str=None, menu_type: str=None) -> list[dict]:
		"""
		Whichever param is filled will change the query:
		-	If vendor_id=upper cafe's ID it will display upper cafe menus
		-	If menuItem = Coffee it will find menu with coffee
	 	-	Null for all should return all menus
		:param vendor_name: Name of the vendor
		:param item_name: Name of the Menu Item
		:param menu_type: Breakfast, Lunch, Dinner, or General
		:return: A list containing menus as dictionaries.
		"""
		query = {}

		if vendor_name:
			query["vendor"] = vendor_name.title()

		if item_name:
			query["menuItem.name"] = {"$regex": item_name, "$options": "i"}		# Case insensitivity to match upper and lower cases

		if menu_type:
			query["type"] = menu_type.title()	# Capitalizes the string

		result = self.__menu.find(query)
		return result.to_list()

	#by type and/or by vendor
	# both params are used it will display the menu with both conditions
	def get_one_menu(self, vendor_name: str, menu_type: str) -> dict:
		"""
		Find one particular menu.
		:param vendor_name: Name of the vendor
		:param menu_type: Breakfast, Lunch, Dinner, or General
		:return: A dictionary containing menu info
		"""
		query = {
			"vendor": vendor_name.title(),
			"type": menu_type.title()
		}
		return self.__menu.find_one(query)

	#used by view Item or view all items
	# with param means display one menu item
	# with param = null display all menus
	def get_menu_item(self, item_name: str = None) -> dict:
		"""
		Get a menu item by its name.
		:param item_name: Name of the Menu Item
		:return: A dictionary containing menu item info
		"""
		if item_name:
			result = self.__menu.aggregate([                    #runs aggregation pipeline against menu collection and converts it into a list
				{"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
				{"$match": {"menuItem.name": {"$regex": item_name, "$options": "i"}}}, #filters to where only the matching item remains
				{"$project": {                                   #selects only the fields required and ignores the rest
					"name": "$menuItem.name",
					"price": "$menuItem.price",
					"description": "$menuItem.description",
					"inStock": "$menuItem.inStock",
					"allergens": "$menuItem.allergens",          #from "name" till this line, pulls fields from the unwound menuItem and allows acess as just item["name"]
					"vendor": "$vendor",
					"menuType": "$type",                         #these two lines pull fields from the menu document to find location and menuType the item belongs
				}},
				{"$limit": 1}
			])
			return result.to_list()[0]

		# Why is this here??
		# I guess it could be useful to get a list of all available menu items....
		# But the way this is described in the comments is that it's supposed to display all menus...
		# We have get_all_menus() for that.
		"""result = self.__menu.aggregate([                     #runs the aggregation pipeline on the menu collection and converts it to the python list
				{"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
				{"$project": {                                   #selects the fields we want to output
					"name": "$menuItem.name",
					"price": "$menuItem.price",
					"description": "$menuItem.description",
					"inStock": "$menuItem.inStock",              #pulls the four fields from the unwound menuItem in the form item["name"], item["price"] and such
					"vendor": "$vendor",
					"menuType": "$type",                         #pulling these two fields from the menu document to find the location and menuType for each item
				}},
				{"$sort": {"vendor": 1, "menuType": 1, "name": 1}} #sorts the results by vendor, then menuType and then name alphabetically, grouping the output logically by place, type and such
			])"""

		return result.to_list()

	# Order functions

	def search_menu_items(self, keyword: str, menu_type: str=None) -> list[dict]:
		"""
		Searches all menu item names by keyword, with Menu Type as an optional criteria as well.
		:param menu_type: (optional) Breakfast, Lunch, Dinner, or General
		:param keyword: A keyword string to search for
		:return: A list of menu items that match the keyword
		"""
		pipeline = []
 
		if menu_type:
			pipeline.append({"$match": {"type": menu_type}})	#filtering by menu type first
 
		pipeline.append({"$unwind": "$menuItem"})				#unwinding the menuItem array

		pipeline.append(
			{"$match": {"menuItem.name": {"$regex": keyword, "$options": "i"}}}
		)													#checking for the match
 
		pipeline.append({"$project": {
			"name": "$menuItem.name",
			"price": "$menuItem.price",
			"description": "$menuItem.description",
			"inStock": "$menuItem.inStock",
			"allergens": "$menuItem.allergens",
		}})
 
		result = self.__menu.aggregate(pipeline)
		return result.to_list()									#returning the matching menu item documents


	#order functions
	# for order identification we are using the given _id from mongodb
	def create_order(self, building: str, room: str, subtotal: float, instructions: str, customer: str, vendor: str, cart: list[dict]) -> str:
		"""
		Creates a new order document and sets all the properties named in the parameter list:
		:param building: A 3-digit string number between 100 and 499
		:param room: A 3- or 4-digit string number between 100 and 599 (the 4th optional digit is a letter, e.g. '315a')
		:param subtotal: The subtotal cost of the order
		:param instructions: Any special instructions given by the user (leave as empty string if none)
		:param customer: The VIU ID of the customer
		:param vendor: The name of the vendor
		:param cart: A list of menu items
		:return: the _id of the order that was just created
		"""
		order_doc = {
			"building": building,
			"room": room,
			"subTotal": subtotal,
			"specialInstructions": instructions,
			"customer": customer,
			"vendor": vendor.title(),	# Make sure vendor name is capitalized properly
			"cartItem": cart,
			"orderStatus": "Pending",
			"orderTime": datetime.now(),
   
			"readyTime": None,
			"acceptTime": None,
			"pickupTime": None,
			"deliveryTime": None,
			"confirmationTime": None,
			"agent": "",										#do we not need these?
		}

		result = self.__order.insert_one(order_doc)
		return str(result.inserted_id)


	def get_order_by_id(self, order_id: str) -> dict:
		"""
		Get an order by its _id
		:param order_id: The _id of the order
		:return: a Python dictionary containing all the information about the order with that ID.
		"""
		result = self.__order.find_one({"_id": ObjectId(order_id)})
		return result

	def get_orders_by_user(self, user_id: str) -> list[dict]:
		"""
		Get all orders by a VIU ID (matches to Agents and Customers)
		:param user_id: The VIU ID of a Customer or Agent
		:return: A Python dictionary containing all the information about the orders with that VIU ID.
		"""
		result = self.__order.find({
			"$or": [
				{"customer": user_id},
				{"agent": user_id}
			]
		})
		return result.to_list()

	def get_all_orders(self) -> list[dict]:
		"""
		Get all orders (for developer access reasons)
		"""
		result = self.__order.find()
		return result.to_list()									#returning all the orders (lets have this for defveloper access)

	def add_agent_to_order(self, order_id: str, agent_id: str) -> int:
		"""
		Find and order by its ID and add the agent’s ID to it.
		:param order_id: VIU ID of the order
		:param agent_id: VIU ID of the agent
		:return: 1 if the order was updated, 0 if not
		"""
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},
			{"$set": {"agent": agent_id}}
		)
		return result.modified_count

	def update_order_status(self, order_id: str, status: str) -> int:
		"""
		Change the status of an order.
		:param order_id: _id of the order
		:param status: "Pending", "ReadyForPickup", "InTransit", "Delivered", or "Received"
		:return: 1 if successful, 0 if not
		"""
		result = self.__order.update_one(
			{"_id": ObjectId(order_id)},						#specific ID we got to change it for
			{"$set": {"orderStatus": status}}					#changing the order status
		)
		return result.modified_count

	"""
	All of the following updaate_<DB_property>Time functions are used to change
	the time of database order properties.
	:param time: a datetime object you want to change the time to.
	:param order_id: _id of the order
	"""

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

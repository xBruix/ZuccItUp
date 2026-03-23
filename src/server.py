# Authors: Caleb, Keenan

from pymongo import MongoClient as MangoClient


class Server:
	# Creates the MangoDB client, connects to the database, and gets the collections.
	def __init__(self, user_ID: str, passwd: str):
		# DEBUG
		# print("Username: " + user_ID)
		# print("Password: " + passwd)

		# Name of the project you want to connect to, e.g. csci375a_project
		self.__project = user_ID + "_project"

		# URI of the MangoDB server
		self.__uri = (f"mongodb://{user_ID}:{passwd}"
					  f"@studb-mongo.csci.viu.ca:27017/"
					  f"{self.__project}?authSource=admin"
					  )

		# Create DB Client or throw an exception if the user ID or password is incorrect.
		try:
			self.__client = MangoClient(self.__uri)
			self.__db = self.__client.get_database(self.__project)
			# Ping the database to check that username and password are actually correct
			self.__db.command("ping")
		except Exception as e:
			# Username and/or password were NOT correct
			raise ValueError("Could not connect to MongoDB: username or password was incorrect")
		else:
			# Get collections as private attributes
			self.__user = self.__db["user"]
			self.__menu = self.__db["menu"]
			self.__order = self.__db["order"]

	# Must call this to disconnect from the server
	def disconnect(self):
		self.__client.close()

	#See code plan in A6 document for details on each function

	#user functions
	def verify_user(self, viu_ID):

		is_valid = False

		return is_valid

	def create_user(eself, mail, name, viu_ID, role):

		return

	def deactivate_user(self, viu_ID):

		return

	def view_user(self, viu_ID):

		return


	#menu functions
	def get_vendors(self):

		return

	def get_all_menu(self, vendor_ID):

		return

	def get_one_menu(self, menu_ID):

		return

	def get_menu_item(self, menu_item_ID):

		return

	#order functions
	def create_order(self, building,room,subtotal,instructions,customer,vendor,cart):

		return

	def get_order(self, order_ID):

		return

	def get_order_by_user(self, user_ID):

		return

	def add_agent_to_order(self, agent_ID, order_ID):

		return

	def update_orderTime(self, time, order_ID):

		return

	def update_readyTime(self, time,order_ID):

		return

	def update_acceptTime(self, time,order_ID):

		return

	def update_pickupTime(self, time,order_ID):

		return

	def update_deliveryTime(self, time,order_ID):

		return

	def update_confirmationTime(self, time,order_ID):

		return
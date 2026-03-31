# Authors: Surya Balram, Bruce Fernandes

# This file defines all user-related classes for the system.
# It includes a base User class and specialized subclasses:
# DeliveryAgent, Customer, and Vendor.

from server import Server
from debug import DEBUG_MODE		# for debug mode
from copy import copy				# for making shallow copies of parent classes
from datetime import datetime		# for handling times and dates
from prettytable import PrettyTable
# See how to use PrettyTable: https://pypi.org/project/prettytable/

class User:
	# Constructor for the base User class
	# Initializes common attributes shared by all users
	def __init__(self, svr: Server):
		self._server = svr
		# The following attributes are protected -- i.e. they can be accessed by Customer and DeliveryAgent, but nothing else
		self._role = ""			# Assigned later, when user logs in
		self._current_user = ""	# VIU ID of the current user
		self._name = ""
		self._email = ""
		self._active = False

	# Getters
	# These return a user attribute, e.g. get_current_user returns the VIU ID of the user who is currently logged in
	def get_current_user(self):
		return self._current_user
	def get_role(self):
		return self._role
	def get_name(self):
		return self._name
	def get_email(self):
		return self._email
	def is_active(self):
		return self._active


	def login(self, viu_id: str, password: str) -> bool:
		"""
		Logs the user in and checks if the user exists.
		:return: True if user is in the database, False if they are not in the database
		"""
		is_in_db = self._server.verify_user(viu_id, password)
		if is_in_db:
			user_data = self._server.view_user(viu_id)
			self._current_user = viu_id
			self._role = user_data["role"]
			self._name = user_data["name"]
			self._email = user_data["email"]
			self._active = user_data["active"]

			if DEBUG_MODE:
				print("Current user: ", self._current_user)
				print("Role: ", self._role)
		return is_in_db

	def logout(self):
		"""Resets the current user to empty"""
		self._current_user = ""
		self._role = ""

	def signup(self, viu_id: str, passwd: str, name: str, email: str, role: str) -> bool:
		"""Creates a new user"""
		try:
			if role.lower() == "agent":		# then we need to need add availability status
				self._server.create_user(viu_id=viu_id, passwd=passwd, name=name, email=email, role=role, availability_status=True)
			else:
				self._server.create_user(viu_id=viu_id, passwd=passwd, name=name, email=email, role=role)
			self._current_user = viu_id
			self._role = role.lower()
			user_data = self._server.view_user(viu_id)
			self._name = user_data["name"]
			self._email = user_data["email"]
			self._active = user_data["active"]
			return True
		except ValueError:
			return False

	def is_logged_in(self):
		return self._current_user != ""
# end User class

# Agent

class DeliveryAgent(User):
	def __init__(self, svr: Server, user_instance: User):
		"""
		A Delivery Agent is a user type of the more general User class.
		This class contains business-layer functions that only the Delivery Agent uses.
		:param svr: A Server object to make database calls
		:param user_instance: A User object that will be symbolically linked to this class
		"""
		self._server = svr
		self.__user_ref = user_instance
		# Set availability status to false if the user instance if empty.
		# Otherwise, find the user's availability status in the DB.
		user_data = svr.view_user(self.__user_ref._current_user)
		self.__availability_status = False if user_data is None else user_data["availabilityStatus"]

	# @property is what's called a decorator.
	# A decorator basically adds additional stuff to a function.
	# In this case, @property sets DeliveryAgent._current_user to be EXACTLY the same as User._current_user
	# It's like creating a symbolic link between the attributes of User and the attributes of DeliveryAgent.
	# This is relevant because if you, say, were logged in as agent 1, like this:
	# 	- User._current_user = "1"
	# 	- DeliveryAgent._current_user = "1"
	#  ...And then you change User._current_user to "2", now it looks like:
	# 	- User._current_user = "2"
	# 	- DeliveryAgent._current_user = "2"
	# This way, you can easily change attributes that are shared across all the classes in this file.
	#
	# Please note that you don't call these functions the way you normally would.
	# These functions are really more like attributes.
	# If you want to access an attribute, use the get functions in User.
	# 	- e.g. agent.get_current_user() will return the current user's VIU ID.
	# DO NOT try to use agent._current_user -- this will not work!!!
	@property
	def _current_user(self):
		return self.__user_ref._current_user
	@property
	def _role(self):
		return self.__user_ref._role
	@property
	def _name(self):
		return self.__user_ref._name
	@property
	def _email(self):
		return self.__user_ref._email
	@property
	def _active(self):
		return self.__user_ref._active

	# Retrieves the agent's availability status
	def get_availability_status(self):
		return self.__availability_status

	# Creates a new delivery agent in the system
	def createAgent(self):
		#finding if the db already has an agent with the given VIUID
		if self._server.verify_user(self._current_user):
			print(f"Agent with VIUID {self._current_user} already exists.")
			return None                                                         #error message if the user already exists
		result = self._server.create_user(
			self._email, self._name, self._current_user, "agent", self.__availability_status
		)                                                                       #inserting the agent into the db
		print(f"Agent '{self._name}' created successfully.")

		return result                                                           #now we print the ID as is in the db

	# Returns details of a specific delivery agent
	def viewAgent(self):
		agent = self._server.view_user(self._current_user)                               #search for the VIUID since that is the unique marker

		if not agent:
			print(f"No agent found with VIUID {self._current_user}.")
			return None                                                         #if the ID does not belong to an agent then tough luck
 
		status = "Available" if agent.get("availabilityStatus") else "Unavailable"  #status must be made

		print("\n" + "─" * 40)                                                  #divider
		print(f"  Name:       {agent.get('name')}")
		print(f"  Email:      {agent.get('email')}")
		print(f"  VIUID:      {agent.get('VIUID')}")
		print(f"  Status:     {status}")                                        #printing the lovely details
		print("─" * 40)                                                         #divider

		return agent                                                            #returns the agent as is

	# Returns a list of all delivery agents
	def viewAllAgents(self):
		agents = self._server.view_all_users("agent")     #kw                            #we want a list of the agents
		if not agents:                                                          #NO AGENTS?!?!?!!?
			print("No delivery agents found.")
			return []                                                           #returning a list since if we don't it might break the caller of this function
 
		print(f"\n{'Name':<25} {'VIUID':<12} {'Email':<30} Status")             #lets make a table with spacing
		print("─" * 75)                                                         #divider be like

		for agent in agents:                                                    #agent here is the actual agent, agents is our list of agents
			status = "Available" if agent.get("availabilityStatus") else "Unavailable"
			print(
				f"{agent.get('name', ''):<25} "
				f"{agent.get('VIUID', ''):<12} "
				f"{agent.get('email', ''):<30} "
				f"{status}"                                                     #lets print all that we need to print
			)
		return agents                                                           #returning the list of agents

	# Verifies the VIU ID of the delivery agent
	def verifyVIUID(self):


		result = self._server.verify_user(self._current_user)       #lets find the agent to see if they exist

		if result:
			print(f"VIUID {self._current_user} verified for agent '{self._name}'.")
			return True                                                         #if verified, less print it
		print(f"VIUID {self._current_user} could not be verified.")
		return False                                                            #unverified

	def setAvailability(self, status: bool):
		self._server.update_availability(self._current_user, status)                     #lets find and update the status if we find the agent
		self.__availability_status = status
		print(f"Agent '{self._name}' is now {'available' if status else 'unavailable'}.")    #appropriate message
 
#──────────────────────────────────────────────
# Customer
#────────────────────────────────────────────── 

# Represents a customer who can place orders
class Customer(User):
	def __init__(self, svr: Server, user_instance: User):
		"""
		A Customer is a user type of the more general User class.
		This class contains business-layer functions that only the Customer uses.
		:param svr: A Server object to make database calls
		"""
		self._server = svr
		self.__user_ref = user_instance
		# Set previously_ordered to an empty list if the user instance is empty.
		# Otherwise, get a list of previously ordered items from the DB.
		user_data = svr.view_user(self.__user_ref._current_user)
		self.__previously_ordered = [] if user_data is None else user_data["previouslyOrdered"]

	@property
	def _current_user(self):
		return self.__user_ref._current_user
	@property
	def _role(self):
		return self.__user_ref._role
	@property
	def _name(self):
		return self.__user_ref._name
	@property
	def _email(self):
		return self.__user_ref._email
	@property
	def _active(self):
		return self.__user_ref._active

	# Prints out the names of all the vendors
	def list_vendors(self) -> int:
		vendor_table = PrettyTable()
		vendor_table.align = "l"		# Align contents to the left
		vendor_table.field_names = ["No.", "Vendor", "Location", "Hours of Operation", "Currently Open", "Email"]		# Columns

		# Add vendors as rows in the table
		vendors = self._server.view_all_users("Vendor")
		for i in range(len(vendors)):
			hrs_of_op = vendors[i]["hoursOfOperation"]	# Shorthand for hoursOfOperation, cos it's a long one
			start = datetime.strptime(hrs_of_op["startTime"], "%H:%M")	# Get startTime as datetime object
			end = datetime.strptime(hrs_of_op["endTime"], "%H:%M")		# Get endTime as datetime object
			is_open = start <= datetime.now() <= end							# Check if the current time is between start and end

			vendor_table.add_row([
				f"{i + 1}",								# No.
				vendors[i]["name"],						# Vendor
				vendors[i]["location"],					# Location
				hrs_of_op["days"] + ", " + hrs_of_op["startTime"] + " - " + hrs_of_op["endTime"],	# e.g. "Mon-Fri, 7:30 - 19:00"
				"Yes" if is_open else "No",				# Currently Open
				vendors[i]["email"],					# Email
			])
		print(vendor_table)
		return len(vendors)

	# Creates a new customer in the system
	def createCustomer(self):

		if self._server.verify_user(self._current_user):
			print(f"Customer with VIUID {self._current_user} already exists.")          #if it exists, why create??????
			return None

		"""
		customer_doc = {
			"name": self.name,
			"email": self.email,
			"VIUID": self.VIUID,
			"role": self.role,
			"previouslyOrdered": self.previouslyOrdered,
		}  """                                                                  #details of the customer to add to the db

		#result = db.user.insert_one(customer_doc)
		result = self._server.create_user(self._email,self._name,self._current_user,"customer")        #kw
		print(f"Customer '{self._name}' created successfully.")                  #done yay
		return result                                            #returning the ID as inserted into mangoDB

	# Returns details of a specific customer
	def viewCustomer(self):

		customer = self._server.view_user(self._current_user)

		if not customer:
			print(f"No customer found with VIUID {self._current_user}.")
			return None                                                         #can't view someone that does not exist
 
		previously = ", ".join(customer.get("previouslyOrdered", [])) or "None" #adding the previously ordered items

		print("\n" + "─" * 40)                                                  #divider
		print(f"  Name:               {customer.get('name')}")
		print(f"  Email:              {customer.get('email')}")
		print(f"  VIUID:              {customer.get('VIUID')}")
		print(f"  Previously Ordered: {previously}")                            #printing the details of the customer
		print("─" * 40)                                                         #divider be like

		return customer                                                         #returning the customer to the caller

	# Returns a list of all customers
	def viewAllCustomers(self):

		customers = self._server.view_all_user("customer")    #kw               #pulling the list of customers from Mango

		if not customers:
			print("No customers found.")
			return []                                                           #returning an empty list if there are no customers
 
		print(f"\n{'Name':<25} {'VIUID':<12} {'Email'}")                        #lets make a table
		print("─" * 60)                                                         #divider

		for customer in customers:
			print(
				f"{customer.get('name', ''):<25} "
				f"{customer.get('VIUID', ''):<12} "
				f"{customer.get('email', '')}"
			)                                                                   #printing each customer and their details side by side

		return customers                                                        #returning the list of customers

	# Verifies the VIU ID of the customer
	def verifyVIUID(self):


		result = self._server.verify_user(self._current_user)       #lets find the agent to see if they exist

		if result:
			print(f"VIUID {self._current_user} verified for Customer '{self._name}'.")
			return True                                                         #if verified, less print it
		print(f"VIUID {self._current_user} could not be verified.")
		return False

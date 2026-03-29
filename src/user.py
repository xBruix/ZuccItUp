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
		self.__role = ""			# Assigned later, when user logs in
		self.__current_user = ""	# Assigned later, when user logs in
		self.__server = svr

	# Getters
	def get_current_user(self):
		return self.__current_user

	def get_role(self):
		return self.__role

	def login(self, viu_id: str, password: str) -> bool:
		"""
		Logs the user in and checks if the user exists.
		:return: True if user is in the database, False if they are not in the database
		"""
		is_in_db = self.__server.verify_user(viu_id, password)
		if is_in_db:
			self.__current_user = viu_id
			self.__role = self.__server.view_user(viu_id)["role"]

			if DEBUG_MODE:
				print("Current user: ", self.__current_user)
				print("Role: ", self.__role)
		return is_in_db

	def logout(self):
		"""Resets the current user to empty"""
		self.__current_user = ""
		self.__role = ""

	def signup(self, viu_id: str, passwd: str, name: str, email: str, role: str) -> bool:
		"""Creates a new user"""
		try:
			if role.lower() == "agent":		# then we need to need add availability status
				self.__server.create_user(viu_id=viu_id, passwd=passwd, name=name, email=email, role=role, availability_status=True)
			else:
				self.__server.create_user(viu_id=viu_id, passwd=passwd, name=name, email=email, role=role)
			self.__current_user = viu_id
			self.__role = role
			return True
		except ValueError:
			return False

	def is_logged_in(self):
		return self.__current_user != ""
# end User class

# Agent

class DeliveryAgent(User):
	# This __init__ allows us to create an Agent in two ways:
	# 	1. Using all the normal parameters: name, email, VIU ID, etc...
	# 	2. Creating an Agent from an instance of a User
	# It's a bit complicated and I had to google all of this, so here's the Stackoverflow link that explains it:
	# https://stackoverflow.com/questions/24921258/python-construct-child-class-from-parent
	#
	# Also here is the W3Schools link to explain what super() does:
	# https://www.w3schools.com/python/python_inheritance.asp
	#
	# Also also here is an explanation of wtf self.__dict__ means:
	# https://realpython.com/python-dict-attribute/
	def __init__(self, svr: Server, *args):
		"""
		A Delivery Agent is a user type of the more general User class.
		This class contains business-layer functions that only the Delivery Agent uses.
		:param svr: A Server object to make database calls
		:param args: An optional argument. If included, this makes a shallow copy of
					the User object passed as an argument. This means that when an attribute
					of the User object changes, the Agent's attributes will also change.
		:raises ValueError: If *args contains anything that isn't a User object.
		"""
		if len(args) == 1:			# Make a shallow copy of the User object passed in
			if type(args[0]) is User:
				self.__dict__ = copy(args[0].__dict__)
			else:
				raise ValueError("Invalid argument type in DeliveryAgent.__init__(). *args only accepts a User object")
		else:
			super().__init__(svr)	# Use __init__() from User class
		self.__availability_status = False	# Should this be True or False by default?

	def get_availability_status(self):
		return self.__availability_status

	# Creates a new delivery agent in the system
	def createAgent(self):
		#finding if the db already has an agent with the given VIUID
		if self.server.verify_user(self.VIUID):
			print(f"Agent with VIUID {self.VIUID} already exists.")
			return None                                                         #error message if the user already exists

		"""agent_doc = {
			"name": self.name,
			"email": self.email,
			"VIUID": self.VIUID,
			"role": self.role,
			"availabilityStatus": self.availabilityStatus,                      # defining the agent to be added to the db with the required details
		}
		result = db.user.insert_one(agent_doc)
										  """
		#kw
		result = self.server.create_user(
			self.email, self.name, self.VIUID, "agent", self.availabilityStatus
		)                                                                       #inserting the agent into the db
		print(f"Agent '{self.name}' created successfully.")

		return result                                                           #now we print the ID as is in the db

	# Returns details of a specific delivery agent
	def viewAgent(self):
		agent = self.server.view_user(self.VIUID)                               #search for the VIUID since that is the unique marker

		if not agent:
			print(f"No agent found with VIUID {self.VIUID}.")
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
		agents = self.server.view_all_user("agent")     #kw                            #we want a list of the agents
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


		result = self.server.verify_user(self.VIUID)       #lets find the agent to see if they exist

		if result:
			print(f"VIUID {self.VIUID} verified for agent '{self.name}'.")
			return True                                                         #if verified, less print it
		print(f"VIUID {self.VIUID} could not be verified.")
		return False                                                            #unverified

	def setAvailability(self, status: bool):
		self.server.update_availability(self.VIUID, status)                     #lets find and update the status if we find the agent
		self.availabilityStatus = status
		print(f"Agent '{self.name}' is now {'available' if status else 'unavailable'}.")    #appropriate message
 
#──────────────────────────────────────────────
# Customer
#────────────────────────────────────────────── 

# Represents a customer who can place orders
class Customer(User):
	def __init__(self, svr: Server, *args):
		"""
		A Customer is a user type of the more general User class.
		This class contains business-layer functions that only the Customer uses.
		:param svr: A Server object to make database calls
		:param args: An optional argument. If included, this makes a shallow copy of
					the User object passed as an argument. This means that when an attribute
					of the User object changes, the Customer's attributes will also change.
		:raises ValueError: If *args contains anything that isn't a User object.
		"""
		if len(args) == 1:			# Make a shallow copy of the User object pass in
			if type(args[0]) is User:
				self.__dict__ = copy(args[0].__dict__) 		# shallow copy
			else:
				raise ValueError("Invalid argument type in Customer.__init__(). *args only accepts a User object")
		else:
			super().__init__(svr)	# Use __init__() from User class
		self.previouslyOrdered = []		# Not sure this is needed?

	# Prints out the names of all the vendors
	def list_vendors(self) -> int:
		vendor_table = PrettyTable()
		vendor_table.align = "l"		# Align contents to the left
		vendor_table.field_names = ["No.", "Vendor", "Location", "Hours of Operation", "Currently Open", "Email"]		# Columns

		# Add vendors as rows in the table
		vendors = self.__server.view_all_users("Vendor")
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

		if self.server.verify_user(self.VIUID):
			print(f"Customer with VIUID {self.VIUID} already exists.")          #if it exists, why create??????
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
		result = self.server.create_user(self.email,self.name,self.VIUID,"customer")        #kw
		print(f"Customer '{self.name}' created successfully.")                  #done yay
		return result                                            #returning the ID as inserted into mangoDB

	# Returns details of a specific customer
	def viewCustomer(self):

		customer = self.server.view_user(self.VIUID)

		if not customer:
			print(f"No customer found with VIUID {self.VIUID}.")
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

		customers = self.server.view_all_user("customer")    #kw               #pulling the list of customers from Mango

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


		result = self.server.verify_user(self.VIUID)       #lets find the agent to see if they exist

		if result:
			print(f"VIUID {self.VIUID} verified for Customer '{self.name}'.")
			return True                                                         #if verified, less print it
		print(f"VIUID {self.VIUID} could not be verified.")
		return False

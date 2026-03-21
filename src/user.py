# Authors: Surya Balram

# This file defines all user-related classes for the system.
# It includes a base User class and specialized subclasses:
# DeliveryAgent, Customer, and Vendor.

class User:
    # Constructor for the base User class
    # Initializes common attributes shared by all users
    def __init__(self, name: str, email: str, role: str):

        self.name = name
        self.email = email
        self.role = role

# DeliveryAgent class inherits from User
# Represents delivery personnel in the system
class DeliveryAgent(User):
    # Constructor for DeliveryAgent
    # Adds VIU ID and availability status to base User attributes
    def __init__(self, availibilityStatus: bool, VIUID: int, name: str, email: str, role: str):

        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.availibilityStatus = availibilityStatus

    # Creates a new delivery agent in the system
    def createAgent(self):
        pass

    # Returns details of a specific delivery agent
    def viewAgent(self):
        pass
        
    # Returns a list of all delivery agents
    def viewAllAgents(self):
        pass

    # Verifies the VIU ID of the delivery agent
    def verifyVIUID(self):
        pass

# Customer class inherits from User
# Represents a customer who can place orders
class Customer(User):

    # Constructor for Customer
    # Adds VIU ID and tracks previous orders
    def __init__(self, VIUID: int, name: str, email: str, role: str):
        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.previouslyOrdered

    # Creates a new customer in the system
    def createCustomer(self):
        pass

    # Returns details of a specific customer
    def viewCustomer(self):
        pass

    # Returns a list of all customers
    def viewAllCustomers(self):
        pass

    # Verifies the VIU ID of the customer
    def verifyVIUID(self):
        pass

# Vendor class inherits from User
# Represents a food vendor on campus
class Vendor(User):

    # Constructor for Vendor
    # Stores vendor location and hours of operation
    def __init__(self, location: str, hoursOfOperations: list, name: str, email: str, role: str):
        User.__init__(self, name, email, role)
        self.location = location
        self.hoursOfOperations = hoursOfOperations

    # Returns details of a specific vendor
    def viewVendor(self):
        pass

    # Returns a list of all vendors
    def viewAllVendors(self):
        pass

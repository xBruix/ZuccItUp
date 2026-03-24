# Authors: Surya Balram, Bruce Fernandes

# This file defines all user-related classes for the system.
# It includes a base User class and specialized subclasses:
# DeliveryAgent, Customer, and Vendor.
import server

class User:
    # Constructor for the base User class
    # Initializes common attributes shared by all users
    def __init__(self, name: str, email: str, role: str):

        self.name = name
        self.email = email
        self.role = role


#──────────────────────────────────────────────
# Agent
#──────────────────────────────────────────────

class DeliveryAgent(User):
    # Constructor for DeliveryAgent
    # Adds VIU ID and availability status to base User attributes
    def __init__(self, availibilityStatus: bool, VIUID: int, name: str, email: str, role: str):

        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.availibilityStatus = availibilityStatus

    # Creates a new delivery agent in the system
    def createAgent(self):
        existing = db.user.find_one({"VIUID": self.VIUID, "role": "Agent"})     #finding if the db already has an agent with the given VIUID
        if existing:
            print(f"Agent with VIUID {self.VIUID} already exists.")
            return None                                                         #error message if the user already exists
    
        """agent_doc = {
            "name": self.name,
            "email": self.email,
            "VIUID": self.VIUID,
            "role": self.role,
            "availabilityStatus": self.availibilityStatus,                      # defining the agent to be added to the db with the required details
        }
        result = db.user.insert_one(agent_doc)
                                          """    
        #kw
        result = create_user(self.email,self.name,self.VIUID,"agent",self.availibilityStatus)#inserting the agent into the db  
        print(f"Agent '{self.name}' created successfully.")
        return result.inserted_id                                               #now we print the ID as is in the db

    # Returns details of a specific delivery agent
    def viewAgent(self):
        agent = db.user.find_one({"VIUID": self.VIUID, "role": "Agent"})        #search for the VIUID since that is the unique marker
        
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
        agents = list(view_all_user(agent))      #kw                            #we want a list of the agents
                                                 #view_all_user is not defined and not in camel Case
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

        
        result = db.user.find_one({"VIUID": self.VIUID, "role": "Agent"})       #lets find the agent to see if they exist
        
        if result:
            print(f"VIUID {self.VIUID} verified for agent '{self.name}'.")
            return True                                                         #if verified, less print it
        print(f"VIUID {self.VIUID} could not be verified.")
        return False                                                            #unverified

    def setAvailability(self, status: bool):
        db.user.update_one(
            {"VIUID": self.VIUID, "role": "Agent"},
            {"$set": {"availabilityStatus": status}}
        )                                                                       #lets find and update the status if we find the agent
        self.availibilityStatus = status
        print(f"Agent '{self.name}' is now {'available' if status else 'unavailable'}.")    #appropriate message
 
#──────────────────────────────────────────────
# Customer
#────────────────────────────────────────────── 



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

        if verify_user(self.VIUID):
            existing = True
        
        if existing:
            print(f"Customer with VIUID {self.VIUID} already exists.")          #if it exists, why create??????
            return None
        """
        customer_doc = {
            "name": self.name,
            "email": self.email,
            "VIUID": self.VIUID,
            "role": self.role,
            "previouslyOrdered": self.previouslyOrdered,
        }  """                                                                     #details of the customer to add to the db
    
        #result = db.user.insert_one(customer_doc)
        result = create_user(self.email,self.name,self.VIUID,"customer")       #kw            
        print(f"Customer '{self.name}' created successfully.")                  #done yay
        return result.inserted_id                                               #returning the ID as inserted into mangoDB

    # Returns details of a specific customer
    def viewCustomer(self):
        customer = view_user(self.VIUID)
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
        
        customers = list(view_all_user("customer"))     #kw               #pulling the list of customers from Mango
        
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

        
        result = db.user.find_one({"VIUID": self.VIUID, "role": "Customer"})       #lets find the agent to see if they exist
        
        if result:
            print(f"VIUID {self.VIUID} verified for Customer '{self.name}'.")
            return True                                                         #if verified, less print it
        print(f"VIUID {self.VIUID} could not be verified.")
        return False
    


#IDK IF YOU GUYS WANT ME TO ACTUALLY CODE THIS PART??
#──────────────────────────────────────────────
# vEnDoR
#──────────────────────────────────────────────

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

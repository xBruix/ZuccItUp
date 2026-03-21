class User:
    def __init__(self, name: str, email: str, role: str):

        self.name = name
        self.email = email
        self.role = role

#──────────────────────────────────────────────
# Agent
#──────────────────────────────────────────────
class DeliveryAgent(User):
    def __init__(self, availibilityStatus: bool, VIUID: int, name: str, email: str, role: str):

        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.availibilityStatus = availibilityStatus

    def createAgent(self):
        existing = db.user.find_one({"VIUID": self.VIUID, "role": "Agent"})     #finding if the db already has an agent with the given VIUID
        if existing:
            print(f"Agent with VIUID {self.VIUID} already exists.")
            return None                                                         #error message if the user already exists
    
        agent_doc = {
            "name": self.name,
            "email": self.email,
            "VIUID": self.VIUID,
            "role": self.role,
            "availabilityStatus": self.availibilityStatus,                      # defining the agent to be added to the db with the required details
        }
        result = db.user.insert_one(agent_doc)                                  #inserting the agent into the db  
        print(f"Agent '{self.name}' created successfully.")
        return result.inserted_id                                               #now we print the ID as is in the db

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
        
    def viewAllAgents(self):
        agents = list(db.user.find({"role": "Agent"}))                          #we want a list of the agents
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
class Customer(User):

    def __init__(self, VIUID: int, name: str, email: str, role: str):
        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.previouslyOrdered

    def createCustomer(self):
        existing = db.user.find_one({"VIUID": self.VIUID, "role": "Customer"})  #find if it exists
        
        if existing:
            print(f"Customer with VIUID {self.VIUID} already exists.")          #if it exists, why create??????
            return None
 
        customer_doc = {
            "name": self.name,
            "email": self.email,
            "VIUID": self.VIUID,
            "role": self.role,
            "previouslyOrdered": self.previouslyOrdered,
        }                                                                       #details of the customer to add to the db
        
        result = db.user.insert_one(customer_doc)                   
        print(f"Customer '{self.name}' created successfully.")                  #done yay
        return result.inserted_id                                               #returning the ID as inserted into mangoDB

    def viewCustomer(self):
        customer = db.user.find_one({"VIUID": self.VIUID, "role": "Customer"})  #lets find our if the customer even exists
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

    def viewAllCustomers(self):
        
        customers = list(db.user.find({"role": "Customer"}))                    #pulling the list of customers from Mango
        
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
class Vendor(User):

    def __init__(self, location: str, hoursOfOperations: list, name: str, email: str, role: str):
        User.__init__(self, name, email, role)
        self.location = location
        self.hoursOfOperations = hoursOfOperations

    def viewVendor(self):
        pass

    def viewAllVendors(self):
        pass

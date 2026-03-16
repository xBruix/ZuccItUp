class User:
    def __init__(self, name: str, email: str, role: str):

        self.name = name
        self.email = email
        self.role = role

class DeliveryAgent(User):
    def __init__(self, availibilityStatus: bool, VIUID: int, name: str, email: str, role: str):

        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.availibilityStatus = availibilityStatus

    def createAgent(self):
        pass

    def viewAgent(self):
        pass
        
    def viewAllAgents(self):
        pass

    def verifyVIUID(self):
        pass

class Customer(User):

    def __init__(self, VIUID: int, name: str, email: str, role: str):
        User.__init__(self, name, email, role)
        self.VIUID = VIUID
        self.previouslyOrdered

    def createCustomer(self):
        pass

    def viewCustomer(self):
        pass

    def viewAllCustomers(self):
        pass

    def verifyVIUID(self):
        pass

class Vendor(User):

    def __init__(self, location: str, hoursOfOperations: list, name: str, email: str, role: str):
        User.__init__(self, name, email, role)
        self.location = location
        self.hoursOfOperations = hoursOfOperations

    def viewVendor(self):
        pass

    def viewAllVendors(self):
        pass

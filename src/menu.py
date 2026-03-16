class Menu():
    def __init__(self, type: str, schedule: list, publishStatus: bool):

        self.type = type
        self.schedule = schedule
        self.publishStatus = publishStatus

    def viewMenu(self):
        pass

    def viewAllMenus(self):
        pass

class MenuItem():
    def __init__(self, name: str, price: float, description: str, inStock: bool, allergens: str):

        self.name = name
        self.price = price
        self.description = description
        self.inStock = inStock
        self.allergens = allergens

    def addToCart(self):
        pass

    def viewItem(self):
        pass

    def viewAllItems(self):
        pass
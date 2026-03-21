# Authors: Surya Balram

# This file defines the Menu and MenuItem classes.
# Menu represents a collection of food items available at certain times.
# MenuItem represents an individual item that can be ordered.

class Menu():
    # Constructor for Menu
    # Initializes menu type, schedule, and publish status
    def __init__(self, type: str, schedule: list, publishStatus: bool):

        self.type = type
        self.schedule = schedule
        self.publishStatus = publishStatus

    # Returns or displays details of a specific menu
    def viewMenu(self):
        pass

    # Returns or displays all available menus
    def viewAllMenus(self):
        pass

# MenuItem represents a single food item in a menu
# Includes details such as name, price, description, stock status, and allergens
class MenuItem():
    # Constructor for MenuItem
    # Initializes item details including name, price, and availability
    def __init__(self, name: str, price: float, description: str, inStock: bool, allergens: str):

        self.name = name
        self.price = price
        self.description = description
        self.inStock = inStock
        self.allergens = allergens

    # Adds this item to a user's cart
    def addToCart(self):
        pass

    # Returns or displays details of this menu item
    def viewItem(self):
        pass

    # Returns or displays all menu items
    def viewAllItems(self):
        pass
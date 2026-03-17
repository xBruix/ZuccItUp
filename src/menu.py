class Menu():
    def __init__(self, type: str, schedule: list, publishStatus: bool):

        self.type = type
        self.schedule = schedule
        self.publishStatus = publishStatus

    def viewMenu(self):

       #keyword = input("Search keyword (leave blank for all): ").strip() //Input search term
    #query = {"Type": True} //checking if the menu type is there
    #if keyword:
        #//search for the menu type query=menu
    #items = list(db.items.find(query)) //gives the list of menu items
    #if not items:
        #print("No items found.")
        #return
    #print(f"\n{'#':<4} {'Name':<15} {'Price':>8}  Description") //printing the menu?
    #print("─" * 55) //spacing
    #for i, item in enumerate(items, 1): //
        #print(f"{i:<4} {item['name']:<15} ${item['price']:>7.2f}  {item['description']}")
        # //looping through the list of menuitems
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
        # pseudocode needs database implementation
        #if not orders:
        #    print("You have no orders yet.")
        #    return
        #for order in orders:
        #    print(fmt_order(order))
        #    print()
        pass
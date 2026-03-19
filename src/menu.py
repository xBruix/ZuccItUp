from collections import defaultdict
from DB_init import db


class Menu():
    def __init__(self, type: str, schedule: list, publishStatus: bool):

        self.type = type
        self.schedule = schedule
        self.publishStatus = publishStatus

    def __viewMenu(self):
        keyword = input("Search keyword (leave blank for all): ").strip() #Prompts the search term and removes and accidental spaces
 
        pipeline = [                         #building our mongodb pipeline
            {"$match": {"type": self.type}}, #checking menu type
            {"$unwind": "$menuItem"},        #unwinding the array of menuItem to separate menus
        ]
        if keyword:                          #checks for empty string
            pipeline.append(                 #if keyword is present, filters items whose name field contains the keyword
                {"$match": {"menuItem.name": {"$regex": keyword, "$options": "i"}}} #options makes it case-insensitive
            )
        pipeline.append({"$project": {       #parameters to select fields
            "name": "$menuItem.name",        #all of these tell mangodb to output the field and pull the value from the db
            "price": "$menuItem.price",
            "description": "$menuItem.description",
            "inStock": "$menuItem.inStock",
            "allergens": "$menuItem.allergens",
        }})
 
        items = list(db.menu.aggregate(pipeline)) #running pipeline against the db and makes a plain python list
        if not items:
            print("No items found.")         #if no menu is found then gives this message
            return
 
        print(f"\n{'#':<4} {'Name':<25} {'Price':>8}  {'In Stock':<10}  Description") #prints header row of the table using the <25 >8 <10 to pad each table to a fixed width and column
        print("─" * 75)                      #printing a divider line
        for i, item in enumerate(items, 1):  #looping through each item, enumerate gives index anmd value at each step. starts at 1 instead of 0 for use readablity(normal humans are not computer people)
            stock = "Yes" if item.get("inStock") else "No" #converts boolean "inStock" field to a readable string and safely returns none instead of crashing with a missing field
            print(                           #prints one formatted row per item 
                f"{i:<4} {item.get('name', ''):<25} "
                f"${item.get('price', 0):>7.2f}  " #gives default - if the field ofest not exist in the document
                f"{stock:<10}  "
                f"{item.get('description', '')}"
            )
 


  
        

    def __viewAllMenus(self):
        menus = list(db.menu.find())
        if not menus: 
            print("No menus are currently available.") #if there is no menus present, prints this message
            return
 
        by_location = defaultdict(list)
        for m in menus:
            by_location[m.get("location", "Unknown")].append(m)
 
        for location, location_menus in by_location.items(): # loops through the dictionary with each iteration giving the location name
            print(f"\n{'═' * 60}")
            print(f"  {location}")
            print(f"{'═' * 60}")                             #prints the section header for each location, surrounded by a border and spacing
            for m in location_menus:                         #loops through each indivisual menu document within the location
                sched = m.get("schedule", {})                #reads the schedule field and defaults if empty
                if isinstance(sched, dict):                  #sanity check for schedule as a plain string
                    sched_str = (                            #if it is a dictionary, it builds a readable schedule string by pulling out the day, start and end time and formatting "day1-day2 XX:XX - YY:YY"
                        f"{sched.get('days', '')}  "
                        f"{sched.get('startTime', '')} – {sched.get('endTime', '')}"
                    )
                else:
                    sched_str = str(sched)                   #if it is not a dictionary, it converts whatever it is into a  string directly without crashing
 
                print(f"\n  [{m.get('type', '').capitalize()} Menu]  |  {sched_str}") #printing the sub-heading
                print(f"  {'Name':<25} {'Price':>8}  {'In Stock':<10}  Description") #prints column headings and dividers with spacing
                print("  " + "─" * 72)                       #spacing and divier go brrrrrrrrr
                for item in m.get("menuItem", []):           #loops through menuItem inside the menu document and defaults to empty list if the field is missing
                    stock = "Yes" if item.get("inStock") else "No" #converts boolean into human readable string because we computer science people are bots
                    print(
                        f"  {item.get('name', ''):<25} "     #printing with formatting and spacing
                        f"${item.get('price', 0):>7.2f}  "
                        f"{stock:<10}  "
                        f"{item.get('description', '')}"
                    )

class MenuItem():
    def __init__(self, name: str, price: float, description: str, inStock: bool, allergens: str):

        self.name = name
        self.price = price
        self.description = description
        self.inStock = inStock
        self.allergens = allergens

    def __addToCart(self,cart):
        if not self.inStock: 
            print(f"Sorry, '{self.name}' is currently out of stock.") #no stock means no add cart
            return
        cart.add_to_cart(self.name, 1)                       #add cart if in stock

    def __viewItem(self): 
        result = list(db.menu.aggregate([                    #runs aggregation pipeline against menu collection and converts it into a list
            {"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
            {"$match": {"menuItem.name": {"$regex": f"^{self.name}$", "$options": "i"}}}, #filters to where only the matching item remains
            {"$project": {                                   #selects only the fields required and deletes the rest
                "name": "$menuItem.name",
                "price": "$menuItem.price",
                "description": "$menuItem.description",
                "inStock": "$menuItem.inStock",
                "allergens": "$menuItem.allergens",          #from "name" till this line, pulls fields from the unwound menuItem and allows acess as just item["name"]
                "location": "$location",
                "menuType": "$type",                         #these two lines pull fields from the menu document to find location and menuType the item belongs
            }},
            {"$limit": 1}                                    #stops at the specific item
        ]))
 
        if not result:                                       #if the item is not found we exit the list and print the message
            print(f"Item '{self.name}' was not found in any menu.")
            return None
 
        item = result[0]                                     #since we got atleast one result, we get it at index 0 so we can work with the item fields in the plain dictionary
        stock = "In stock" if item.get("inStock") else "Out of stock"
        allergens = item.get("allergens") or "None"          #reads allegens field, if missinf or empty string will give hte same result
 
        print("\n" + "─" * 50)                               #spacing and divider
        print(f"  Name:        {item.get('name')}")
        print(f"  Price:       ${item.get('price', 0):.2f}")
        print(f"  Description: {item.get('description')}")
        print(f"  Status:      {stock}")
        print(f"  Allergens:   {allergens}")                 #each of the print statements will print separate fields with their own labels and lines with spacing and padding
        print(f"  Location:    {item.get('location')}  ({item.get('menuType', '').capitalize()} Menu)") #this prints where the item is served and which menuType it falls under
        print("─" * 50)                                      #divider line
        return item                                          #returns the item required

    def __viewAllItems(self):
        items = list(db.menu.aggregate([                     #runs the aggregation pipeline on the menu collection and converts it to the python list
            {"$unwind": "$menuItem"},                        #unwinding the array of menuItem to separate menus
            {"$project": {                                   #selects the fields we want to output
                "name": "$menuItem.name",                    
                "price": "$menuItem.price",
                "description": "$menuItem.description",
                "inStock": "$menuItem.inStock",              #pulls the four fields from the unwound menuItem in the form item["name"], item["price"] and such
                "location": "$location",
                "menuType": "$type",                         #pulling these two fields from the menu document to find the location and menuType for each item
            }},
            {"$sort": {"location": 1, "menuType": 1, "name": 1}} #sorts the results by location, then menuType and then name alphabetically, grouping the output logically by place, type and such
        ]))
 
        if not items:
            print("No menu items found.")                    #unlikely but if the database is empty, it will print this
            return []
 
        print(f"\n{'Name':<25} {'Price':>8}  {'In Stock':<10}  {'Location':<15}  Type") #printing headings with spacing
        print("─" * 80)                                      #divider line
        for item in items:
            stock = "Yes" if item.get("inStock") else "No"   #convering booleans to readable yes or no
            print(
                f"{item.get('name', ''):<25} "
                f"${item.get('price', 0):>7.2f}  "
                f"{stock:<10}  "
                f"{item.get('location', ''):<15}  "
                f"{item.get('menuType', '').capitalize()}"   #printing the actual items
            )
        return items                                         #returning items
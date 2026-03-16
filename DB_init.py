from datetime import datetime
from pymongo import MongoClient as MangoClient	# will this work?
import getpass

password = getpass.getpass("Enter your Mango password:\n> ")
uri = f"mongodb://bronnc:{password}@studb-mongo.csci.viu.ca:27017/bronnc_project?authSource=admin"
client = MangoClient(uri)

db = client.get_database("bronnc_project")
menu = db.get_collection("menu")	# collection
order = db.get_collection("order")  

# Lower Cafe - Breakfast Menu (7:30am - 10:30am)
menu.insert_one({
    "type": "Breakfast",
    "publishStatus": True,
    "schedule": [
        "Monday-Friday: 7:30am - 10:30am"
    ],
    "location" : "Lower Cafe",
    "menuItem": [
        # Classic Hot Breakfasts
        {
            "name": "Scrambled Eggs",
            "price": 6.99,
            "description": "Classic scrambled eggs with toast",
            "inStock": True,
            "allergens": "eggs, gluten"
        },
        {
            "name": "Bacon and Eggs",
            "price": 8.99,
            "description": "Two eggs any style with bacon strips and toast",
            "inStock": True,
            "allergens": "eggs, gluten"
        },
        {
            "name": "Sausage and Eggs",
            "price": 8.99,
            "description": "Two eggs any style with breakfast sausages and toast",
            "inStock": True,
            "allergens": "eggs, gluten"
        },
        {
            "name": "Pancakes",
            "price": 7.50,
            "description": "Stack of fluffy pancakes with maple syrup",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "French Toast",
            "price": 7.50,
            "description": "Classic French toast with maple syrup",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Western Omelette",
            "price": 9.50,
            "description": "Three-egg omelette with ham, peppers, onions, and cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        {
            "name": "Veggie Omelette",
            "price": 8.50,
            "description": "Three-egg omelette with seasonal vegetables and cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        
        # Breakfast Bowls
        {
            "name": "Classic Breakfast Bowl",
            "price": 9.99,
            "description": "Scrambled eggs, breakfast potatoes, bacon, and cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        {
            "name": "Veggie Breakfast Bowl",
            "price": 8.99,
            "description": "Scrambled eggs, breakfast potatoes, seasonal vegetables, and cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        {
            "name": "Southwest Breakfast Bowl",
            "price": 10.50,
            "description": "Scrambled eggs, black beans, salsa, avocado, and cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        
        # Fresh Fruit
        {
            "name": "Fresh Fruit Cup",
            "price": 4.50,
            "description": "Assorted seasonal fresh fruit",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Fresh Fruit Bowl",
            "price": 6.50,
            "description": "Large bowl of assorted seasonal fresh fruit",
            "inStock": True,
            "allergens": ""
        },
        
        # Yogurt Parfaits
        {
            "name": "Classic Yogurt Parfait",
            "price": 5.00,
            "description": "Yogurt layered with granola and fresh berries",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Greek Yogurt Parfait",
            "price": 5.50,
            "description": "Greek yogurt with honey, granola, and fresh fruit",
            "inStock": True,
            "allergens": "lactose"
        },
        
        # Muffins (expanded from "various flavours")
        {
            "name": "Blueberry Muffin",
            "price": 3.50,
            "description": "Freshly baked blueberry muffin",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Chocolate Chip Muffin",
            "price": 3.50,
            "description": "Freshly baked chocolate chip muffin",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Bran Muffin",
            "price": 3.50,
            "description": "Healthy bran muffin with raisins",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Banana Nut Muffin",
            "price": 3.50,
            "description": "Moist banana muffin with walnuts",
            "inStock": True,
            "allergens": "gluten, eggs, nuts"
        },
        
        # Pastries (expanded)
        {
            "name": "Croissant",
            "price": 3.00,
            "description": "Buttery flaky croissant",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Chocolate Croissant",
            "price": 3.75,
            "description": "Croissant filled with chocolate",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Almond Croissant",
            "price": 4.00,
            "description": "Croissant with almond filling",
            "inStock": True,
            "allergens": "gluten, lactose, nuts"
        },
        {
            "name": "Danish",
            "price": 3.50,
            "description": "Fruit-filled Danish pastry",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Cinnamon Roll",
            "price": 4.00,
            "description": "Warm cinnamon roll with icing",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Scone",
            "price": 3.25,
            "description": "Freshly baked scone",
            "inStock": True,
            "allergens": "gluten, lactose"
        }
    ]
})

# Lower Cafe - Lunch Menu (11:00am - 2:00pm)
menu.insert_one({
    "type": "Lunch",
    "publishStatus": True,
    "schedule": [
        "Monday-Friday: 11:00am - 2:00pm"
    ],
    "location" : "Lower Cafe",
    "menuItem": [
        # Made-to-Order Burgers (expanded)
        {
            "name": "Classic Burger",
            "price": 12.00,
            "description": "Beef patty with lettuce, tomato, onion, and pickles",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Cheeseburger",
            "price": 13.00,
            "description": "Classic burger with cheddar cheese",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Loaded Burger",
            "price": 15.00,
            "description": "Beef patty with bacon, cheese, sautéed mushrooms, and onions",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Veggie Burger",
            "price": 12.50,
            "description": "Plant-based patty with lettuce, tomato, and special sauce",
            "inStock": True,
            "allergens": "gluten, soy"
        },
        {
            "name": "Chicken Burger",
            "price": 13.50,
            "description": "Grilled chicken breast with lettuce, tomato, and mayo",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        
        # Comfort Foods
        {
            "name": "Beef Dip",
            "price": 14.50,
            "description": "Sliced roast beef on a toasted bun with au jus",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Chicken Strips",
            "price": 10.99,
            "description": "Crispy breaded chicken strips",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Chicken Strips with Fries",
            "price": 13.99,
            "description": "Crispy chicken strips with a side of fries",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "French Fries",
            "price": 5.00,
            "description": "Crispy golden french fries",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Poutine",
            "price": 9.50,
            "description": "Fries topped with gravy and cheese curds",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Loaded Poutine",
            "price": 12.00,
            "description": "Poutine with bacon and green onions",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Chicken Noodle Soup",
            "price": 6.50,
            "description": "House-made chicken noodle soup",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Tomato Basil Soup",
            "price": 6.50,
            "description": "Creamy house-made tomato basil soup",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Soup of the Day",
            "price": 6.50,
            "description": "Chef's daily soup special",
            "inStock": True,
            "allergens": ""
        },
        
        # Sandwiches (expanded from "various types")
        {
            "name": "Ham and Cheddar Sandwich",
            "price": 11.00,
            "description": "Sliced ham with cheddar cheese on fresh bread",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Roast Beef Sandwich",
            "price": 12.00,
            "description": "Tender roast beef with horseradish mayo",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Chicken Caesar Wrap",
            "price": 11.50,
            "description": "Grilled chicken with romaine, parmesan, and caesar dressing in a wrap",
            "inStock": True,
            "allergens": "gluten, lactose, eggs, fish"
        },
        {
            "name": "Falafel Wrap",
            "price": 10.50,
            "description": "Crispy falafel with hummus, veggies, and tahini sauce",
            "inStock": True,
            "allergens": "gluten, sesame"
        },
        {
            "name": "BLT Sandwich",
            "price": 10.00,
            "description": "Bacon, lettuce, and tomato on toasted bread",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Turkey Club",
            "price": 12.50,
            "description": "Triple-decker with turkey, bacon, lettuce, and tomato",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        
        # Salads (expanded from "various types")
        {
            "name": "Cobb Salad",
            "price": 12.00,
            "description": "Mixed greens with chicken, bacon, egg, avocado, and blue cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        {
            "name": "Caesar Salad",
            "price": 10.00,
            "description": "Romaine lettuce with parmesan, croutons, and caesar dressing",
            "inStock": True,
            "allergens": "gluten, lactose, eggs, fish"
        },
        {
            "name": "Caesar Salad with Chicken",
            "price": 13.00,
            "description": "Caesar salad topped with grilled chicken breast",
            "inStock": True,
            "allergens": "gluten, lactose, eggs, fish"
        },
        {
            "name": "House Greens Salad",
            "price": 9.00,
            "description": "Mixed greens with seasonal vegetables and vinaigrette",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Greek Salad",
            "price": 11.00,
            "description": "Tomatoes, cucumbers, olives, feta, and red onion",
            "inStock": True,
            "allergens": "lactose"
        },
        
        # To-Go Meals
        {
            "name": "Lasagna To-Go",
            "price": 12.00,
            "description": "Meat lasagna ready to heat and enjoy",
            "inStock": True,
            "allergens": "gluten, lactose, eggs"
        },
        {
            "name": "Mac and Cheese To-Go",
            "price": 10.00,
            "description": "Creamy mac and cheese ready to heat",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Shepherd's Pie To-Go",
            "price": 11.50,
            "description": "Hearty shepherd's pie ready to heat",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Chicken Alfredo To-Go",
            "price": 13.00,
            "description": "Creamy chicken alfredo pasta ready to heat",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        
        # Light Bites
        {
            "name": "Fresh Fruit Cup",
            "price": 4.50,
            "description": "Assorted seasonal fresh fruit",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Yogurt Parfait",
            "price": 5.00,
            "description": "Yogurt layered with granola and fresh berries",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Blueberry Muffin",
            "price": 3.50,
            "description": "Freshly baked blueberry muffin",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Chocolate Chip Muffin",
            "price": 3.50,
            "description": "Freshly baked chocolate chip muffin",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Banana Nut Muffin",
            "price": 3.50,
            "description": "Moist banana muffin with walnuts",
            "inStock": True,
            "allergens": "gluten, eggs, nuts"
        },
        {
            "name": "Croissant",
            "price": 3.00,
            "description": "Buttery flaky croissant",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Danish",
            "price": 3.50,
            "description": "Fruit-filled Danish pastry",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        }
    ]
})


# Upper Cafe - Breakfast Menu (7:30am - 9:30am)
menu.insert_one({
    "type": "Breakfast",
    "publishStatus": True,
    "schedule": [
        "Monday-Friday: 7:30am - 9:30am"
    ],
    "location" : "Upper Cafe",
    "menuItem": [
        # Muffins (expanded)
        {
            "name": "Chocolate Chip Muffin",
            "price": 3.50,
            "description": "Chocolate Chip Muffin baked on campus",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Blueberry Muffin",
            "price": 3.50,
            "description": "Blueberry Muffin baked on campus",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Bran Muffin",
            "price": 3.50,
            "description": "Healthy bran muffin baked on campus",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Banana Nut Muffin",
            "price": 3.50,
            "description": "Banana muffin with walnuts baked on campus",
            "inStock": True,
            "allergens": "gluten, nuts"
        },
        {
            "name": "Lemon Poppy Seed Muffin",
            "price": 3.50,
            "description": "Fresh lemon poppy seed muffin baked on campus",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        
        # Yogurt
        {
            "name": "Yogurt Parfait",
            "price": 5.00,
            "description": "Yogurt parfait with various fruits",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Greek Yogurt Parfait",
            "price": 5.50,
            "description": "Greek yogurt parfait with honey and granola",
            "inStock": True,
            "allergens": "lactose"
        },
        
        # Bagels (expanded from "various flavours")
        {
            "name": "Everything Bagel",
            "price": 4.00,
            "description": "Everything bagel with sesame, poppy seeds, garlic, and onion",
            "inStock": True,
            "allergens": "gluten, sesame"
        },
        {
            "name": "Plain Bagel",
            "price": 4.00,
            "description": "Classic plain bagel",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Blueberry Bagel",
            "price": 4.00,
            "description": "Blueberry bagel",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Herb and Garlic Bagel",
            "price": 4.00,
            "description": "Herb and garlic seasoned bagel",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Sesame Bagel",
            "price": 4.00,
            "description": "Bagel topped with sesame seeds",
            "inStock": True,
            "allergens": "gluten, sesame"
        },
        {
            "name": "Cinnamon Raisin Bagel",
            "price": 4.00,
            "description": "Sweet cinnamon raisin bagel",
            "inStock": True,
            "allergens": "gluten"
        },
        
        # Bagel with Cream Cheese
        {
            "name": "Everything Bagel with Cream Cheese",
            "price": 5.50,
            "description": "Everything bagel with cream cheese",
            "inStock": True,
            "allergens": "gluten, lactose, sesame"
        },
        {
            "name": "Plain Bagel with Cream Cheese",
            "price": 5.50,
            "description": "Plain bagel with cream cheese",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Blueberry Bagel with Cream Cheese",
            "price": 5.50,
            "description": "Blueberry bagel with cream cheese",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        
        # Additional Breakfast Items
        {
            "name": "Croissant",
            "price": 3.75,
            "description": "Buttery flaky croissant",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Chocolate Croissant",
            "price": 4.25,
            "description": "Croissant filled with chocolate",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Cinnamon Roll",
            "price": 4.50,
            "description": "Warm cinnamon roll with icing",
            "inStock": True,
            "allergens": "gluten, lactose, eggs"
        },
        {
            "name": "Danish",
            "price": 4.00,
            "description": "Fruit-filled Danish pastry",
            "inStock": True,
            "allergens": "gluten, lactose, eggs"
        },
        {
            "name": "Fresh Fruit Cup",
            "price": 4.50,
            "description": "Assorted seasonal fresh fruit",
            "inStock": True,
            "allergens": ""
        }
    ]
})

# Upper Cafe - Lunch Menu (10:30am - 4:00pm)
menu.insert_one({
    "type": "Lunch",
    "publishStatus": True,
    "schedule": [
        "Monday-Friday: 10:30am - 4:00pm"
    ],
    "location" : "Upper Cafe",
    "menuItem": [
        # Chicken Strips
        {
            "name": "Chicken Strips",
            "price": 8.99,
            "description": "6 breaded chicken strips",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Chicken Strips with Fries",
            "price": 13.99,
            "description": "6 breaded chicken strips with a side of fries",
            "inStock": True,
            "allergens": "gluten"
        },
        
        # Sandwiches
        {
            "name": "BLT",
            "price": 12.00,
            "description": "Bacon, lettuce and tomato sandwich",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Turkey Swiss Sandwich",
            "price": 15.00,
            "description": "Roasted turkey on bread with Swiss cheese",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        
        # Sandwiches (expanded from "various types")
        {
            "name": "Ham and Cheddar Sandwich",
            "price": 15.00,
            "description": "Sliced ham with cheddar cheese on fresh bread",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Roast Beef Sandwich",
            "price": 15.00,
            "description": "Tender roast beef with horseradish mayo",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Chicken Caesar Wrap",
            "price": 15.00,
            "description": "Grilled chicken with romaine, parmesan, and caesar dressing in a wrap",
            "inStock": True,
            "allergens": "gluten, lactose, eggs, fish"
        },
        {
            "name": "Falafel Wrap",
            "price": 15.00,
            "description": "Crispy falafel with hummus, veggies, and tahini sauce",
            "inStock": True,
            "allergens": "gluten, sesame"
        },
        {
            "name": "Tuna Melt",
            "price": 13.50,
            "description": "Tuna salad with melted cheese on toasted bread",
            "inStock": True,
            "allergens": "gluten, lactose, fish, eggs"
        },
        {
            "name": "Grilled Cheese",
            "price": 10.00,
            "description": "Classic grilled cheese sandwich",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Club Sandwich",
            "price": 16.00,
            "description": "Triple-decker with turkey, bacon, lettuce, and tomato",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        
        # Pizza (expanded from "various types")
        {
            "name": "Hawaiian Pizza",
            "price": 20.00,
            "description": "Pizza with ham and pineapple",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Margherita Pizza",
            "price": 20.00,
            "description": "Classic pizza with tomato, mozzarella, and basil",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Meat Lovers Pizza",
            "price": 20.00,
            "description": "Pizza loaded with pepperoni, sausage, bacon, and ham",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Pepperoni Pizza",
            "price": 20.00,
            "description": "Classic pepperoni pizza",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Veggie Pizza",
            "price": 20.00,
            "description": "Pizza with assorted vegetables",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "BBQ Chicken Pizza",
            "price": 20.00,
            "description": "Pizza with BBQ sauce, chicken, and red onion",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        
        # Salads (expanded from "various types")
        {
            "name": "Cobb Salad",
            "price": 10.00,
            "description": "Mixed greens with chicken, bacon, egg, avocado, and blue cheese",
            "inStock": True,
            "allergens": "eggs, lactose"
        },
        {
            "name": "Caesar Salad",
            "price": 10.00,
            "description": "Romaine lettuce with parmesan, croutons, and caesar dressing",
            "inStock": True,
            "allergens": "gluten, lactose, eggs, fish"
        },
        {
            "name": "Caesar Salad with Chicken",
            "price": 13.00,
            "description": "Caesar salad topped with grilled chicken breast",
            "inStock": True,
            "allergens": "gluten, lactose, eggs, fish"
        },
        {
            "name": "House Greens Salad",
            "price": 10.00,
            "description": "Mixed greens with seasonal vegetables and vinaigrette",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Greek Salad",
            "price": 11.00,
            "description": "Tomatoes, cucumbers, olives, feta, and red onion",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Spinach Salad",
            "price": 11.50,
            "description": "Fresh spinach with strawberries, walnuts, and balsamic vinaigrette",
            "inStock": True,
            "allergens": "nuts"
        },
        
        # Sides
        {
            "name": "French Fries",
            "price": 5.00,
            "description": "Crispy golden french fries",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Onion Rings",
            "price": 6.00,
            "description": "Crispy battered onion rings",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Poutine",
            "price": 9.00,
            "description": "Fries topped with gravy and cheese curds",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Side Salad",
            "price": 5.50,
            "description": "Small mixed green salad",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Soup of the Day",
            "price": 6.50,
            "description": "Chef's daily soup special",
            "inStock": True,
            "allergens": ""
        }
    ]
})

# Upper Cafe - Dinner Menu (4:00pm - 7:00pm)
# Note: Only Monday items are in stock as per original example
menu.insert_one({
    "type": "Dinner",
    "publishStatus": True,
    "schedule": [
        "Monday-Friday: 4:00pm - 7:00pm"
    ],
    "location" : "Upper Cafe",
    "menuItem": [
        # Monday Specials (In Stock)
        {
            "name": "Chicken Parmesan",
            "price": 15.00,
            "description": "Chicken parmesan with choice of 2: roasted potato, seasonal vegetables, or green salad",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Breaded Eggplant Parmesan",
            "price": 15.00,
            "description": "Breaded eggplant parmesan with choice of 2: roasted potato, seasonal vegetables, or green salad",
            "inStock": True,
            "allergens": "gluten, lactose, eggs"
        },
        
        # Tuesday Specials (Out of Stock)
        {
            "name": "Pork Schnitzel",
            "price": 20.00,
            "description": "Pork Schnitzel with mushroom sauce and choice of seasonal vegetables or mashed potato",
            "inStock": False,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Crispy Pad Thai",
            "price": 15.00,
            "description": "Crispy Pad Thai with rice noodles and vegetables",
            "inStock": False,
            "allergens": "gluten, eggs, peanuts, shellfish"
        },
        
        # Wednesday Specials (Out of Stock)
        {
            "name": "Chicken Pot Pie",
            "price": 17.00,
            "description": "Chicken pot pie with choice of garlic bread or garden salad",
            "inStock": False,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Vegetarian Pot Pie",
            "price": 17.00,
            "description": "Vegetarian pot pie with choice of garlic bread or garden salad",
            "inStock": False,
            "allergens": "gluten, lactose"
        },
        
        # Thursday Specials (Out of Stock)
        {
            "name": "Roast Pork Loin",
            "price": 17.00,
            "description": "Roast pork loin with choice of twice baked potato, seasonal vegetables, or caesar salad",
            "inStock": False,
            "allergens": ""
        },
        {
            "name": "Tofu Banh Mi Sandwich",
            "price": 17.00,
            "description": "Tofu banh mi sandwich with choice of twice baked potato, seasonal vegetables, or caesar salad",
            "inStock": False,
            "allergens": "gluten, soy"
        },
        
        # Friday Specials (Out of Stock)
        {
            "name": "Fish and Chips",
            "price": 14.00,
            "description": "Battered fish with choice of fries, rice, seasonal vegetables, coleslaw, or caesar salad",
            "inStock": False,
            "allergens": "gluten, fish"
        },
        {
            "name": "Ratatouille Wellington",
            "price": 14.00,
            "description": "Ratatouille wellington with choice of fries, rice, seasonal vegetables, coleslaw, or caesar salad",
            "inStock": False,
            "allergens": "gluten"
        },
        
        # Additional Dinner Options
        {
            "name": "Grilled Salmon",
            "price": 22.00,
            "description": "Grilled salmon fillet with lemon butter sauce and choice of 2 sides",
            "inStock": False,
            "allergens": "fish, lactose"
        },
        {
            "name": "Beef Stir Fry",
            "price": 16.00,
            "description": "Beef stir fry with vegetables over rice",
            "inStock": False,
            "allergens": "soy, gluten"
        },
        {
            "name": "Vegetable Curry",
            "price": 14.00,
            "description": "Vegetable curry with rice and naan bread",
            "inStock": False,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Lasagna",
            "price": 16.00,
            "description": "Classic meat lasagna with garlic bread",
            "inStock": False,
            "allergens": "gluten, lactose, eggs"
        },
        {
            "name": "Vegetarian Lasagna",
            "price": 15.00,
            "description": "Vegetable lasagna with garlic bread",
            "inStock": False,
            "allergens": "gluten, lactose, eggs"
        }
    ]
})

# Upper Cafe - All Day Menu (7:00am - 7:00pm)
menu.insert_one({
    "type": "General",
    "publishStatus": True,
    "schedule": [
        "Monday-Friday: 7:00am - 7:00pm"
    ],
    "location" : "Upper Cafe",
    "menuItem": [
        # Coffee
        {
            "name": "Coffee",
            "price": 2.50,
            "description": "Freshly brewed Salt Spring Island coffee",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Espresso",
            "price": 3.00,
            "description": "Single shot of espresso",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Double Espresso",
            "price": 3.75,
            "description": "Double shot of espresso",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Americano",
            "price": 3.25,
            "description": "Espresso with hot water",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Latte",
            "price": 4.50,
            "description": "Espresso with steamed milk",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Cappuccino",
            "price": 4.50,
            "description": "Espresso with steamed milk and foam",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Mocha",
            "price": 5.00,
            "description": "Espresso with chocolate and steamed milk",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Caramel Macchiato",
            "price": 5.25,
            "description": "Espresso with vanilla, steamed milk, and caramel",
            "inStock": True,
            "allergens": "lactose"
        },
        {
            "name": "Iced Coffee",
            "price": 3.75,
            "description": "Cold brewed coffee over ice",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Iced Latte",
            "price": 4.75,
            "description": "Espresso with cold milk over ice",
            "inStock": True,
            "allergens": "lactose"
        },
        
        # Gum (expanded from "various flavours and brands")
        {
            "name": "Spearmint Gum",
            "price": 2.50,
            "description": "Spearmint flavored chewing gum",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Peppermint Gum",
            "price": 2.50,
            "description": "Peppermint flavored chewing gum",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Wintergreen Gum",
            "price": 2.50,
            "description": "Wintergreen flavored chewing gum",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Cinnamon Gum",
            "price": 2.50,
            "description": "Cinnamon flavored chewing gum",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Fruit Gum",
            "price": 2.50,
            "description": "Assorted fruit flavored chewing gum",
            "inStock": True,
            "allergens": ""
        },
        
        # Baked Goods
        {
            "name": "Banana Bread",
            "price": 4.50,
            "description": "Freshly baked banana bread",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Chocolate Chip Cookie",
            "price": 3.00,
            "description": "Freshly baked chocolate chip cookie",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Oatmeal Raisin Cookie",
            "price": 3.00,
            "description": "Freshly baked oatmeal raisin cookie",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "Double Chocolate Cookie",
            "price": 3.00,
            "description": "Rich double chocolate cookie",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        {
            "name": "Brownie",
            "price": 4.00,
            "description": "Fudgy chocolate brownie",
            "inStock": True,
            "allergens": "gluten, eggs, lactose"
        },
        
        # Beverages
        {
            "name": "Iced Tea",
            "price": 3.00,
            "description": "Bottled iced tea",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Lemon Iced Tea",
            "price": 3.00,
            "description": "Bottled lemon iced tea",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Peach Iced Tea",
            "price": 3.00,
            "description": "Bottled peach iced tea",
            "inStock": True,
            "allergens": ""
        },
        
        # Energy Drinks (expanded from "black or white monster")
        {
            "name": "Black Monster",
            "price": 6.50,
            "description": "Monster Energy original black can",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "White Monster",
            "price": 6.50,
            "description": "Monster Energy Ultra white can",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Blue Monster",
            "price": 6.50,
            "description": "Monster Energy blue can",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Red Bull",
            "price": 6.00,
            "description": "Red Bull energy drink",
            "inStock": True,
            "allergens": ""
        },
        
        # Other Drinks
        {
            "name": "Bottled Water",
            "price": 2.00,
            "description": "500ml bottled water",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Sparkling Water",
            "price": 2.50,
            "description": "500ml sparkling water",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Orange Juice",
            "price": 3.50,
            "description": "Fresh orange juice",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Apple Juice",
            "price": 3.50,
            "description": "Fresh apple juice",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Coca-Cola",
            "price": 2.75,
            "description": "Bottled Coca-Cola",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Diet Coke",
            "price": 2.75,
            "description": "Bottled Diet Coke",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Sprite",
            "price": 2.75,
            "description": "Bottled Sprite",
            "inStock": True,
            "allergens": ""
        },
        
        # Snacks
        {
            "name": "Granola Bar",
            "price": 2.50,
            "description": "Chewy granola bar",
            "inStock": True,
            "allergens": "gluten, nuts"
        },
        {
            "name": "Protein Bar",
            "price": 3.50,
            "description": "High protein energy bar",
            "inStock": True,
            "allergens": "nuts, soy"
        },
        {
            "name": "Chips",
            "price": 2.00,
            "description": "Assorted potato chips",
            "inStock": True,
            "allergens": ""
        }
    ]
})



# Unleashed Hot Dogs - All Day Menu
menu.insert_one({
    "type": "General",
    "publishStatus": True,
    "schedule": [
        "Monday-Saturday: 11:00am - 8:00pm"
    ],
    "location" : "Hot Dog",
    "menuItem": [
        # Signature Hot Dogs
        {
            "name": "The Classic",
            "price": 8.50,
            "description": "All-beef hot dog with ketchup, mustard, and relish",
            "inStock": True,
            "allergens": "gluten, mustard"
        },
        {
            "name": "The New Yorker",
            "price": 9.50,
            "description": "All-beef hot dog with sauerkraut, spicy brown mustard, and onions",
            "inStock": True,
            "allergens": "gluten, mustard"
        },
        {
            "name": "The Chicago Dog",
            "price": 10.00,
            "description": "All-beef hot dog with yellow mustard, onions, relish, tomato, pickle, sport peppers, and celery salt on a poppy seed bun",
            "inStock": True,
            "allergens": "gluten, mustard, sesame"
        },
        {
            "name": "The Coney Island",
            "price": 10.50,
            "description": "All-beef hot dog with meat chili, onions, and mustard",
            "inStock": True,
            "allergens": "gluten, mustard"
        },
        {
            "name": "The Seattle Dog",
            "price": 11.00,
            "description": "All-beef hot dog with cream cheese, grilled onions, and jalapeños",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "The Bacon Wrapped",
            "price": 11.50,
            "description": "Bacon-wrapped all-beef hot dog with caramelized onions, peppers, and special sauce",
            "inStock": True,
            "allergens": "gluten, eggs"
        },
        {
            "name": "The Mac Daddy",
            "price": 12.00,
            "description": "All-beef hot dog topped with mac and cheese, bacon bits, and green onions",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "The Chili Cheese Dog",
            "price": 11.00,
            "description": "All-beef hot dog with beef chili, shredded cheddar cheese, and onions",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "The Nacho Dog",
            "price": 11.50,
            "description": "All-beef hot dog with nacho cheese, jalapeños, salsa, and tortilla chips",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "The Hawaiian",
            "price": 10.50,
            "description": "All-beef hot dog with grilled pineapple, teriyaki glaze, and crispy onions",
            "inStock": True,
            "allergens": "gluten, soy"
        },
        {
            "name": "The BBQ Pulled Pork Dog",
            "price": 12.50,
            "description": "All-beef hot dog topped with BBQ pulled pork, coleslaw, and crispy onions",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "The Veggie Dog",
            "price": 9.00,
            "description": "Plant-based hot dog with your choice of toppings",
            "inStock": True,
            "allergens": "gluten, soy"
        },
        
        # Sausages
        {
            "name": "Bratwurst",
            "price": 10.50,
            "description": "Traditional German bratwurst with sauerkraut and mustard",
            "inStock": True,
            "allergens": "gluten, mustard"
        },
        {
            "name": "Italian Sausage",
            "price": 11.00,
            "description": "Spicy Italian sausage with peppers, onions, and marinara sauce",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Chorizo Sausage",
            "price": 11.50,
            "description": "Spicy chorizo with pico de gallo, avocado, and lime crema",
            "inStock": True,
            "allergens": "gluten, lactose"
        },
        {
            "name": "Smokie",
            "price": 9.50,
            "description": "Classic smoked sausage with your choice of toppings",
            "inStock": True,
            "allergens": "gluten"
        },
        
        # Beverages
        {
            "name": "Coca-Cola",
            "price": 2.50,
            "description": "Canned Coca-Cola",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Diet Coke",
            "price": 2.50,
            "description": "Canned Diet Coke",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Sprite",
            "price": 2.50,
            "description": "Canned Sprite",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Root Beer",
            "price": 2.50,
            "description": "Canned root beer",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Iced Tea",
            "price": 2.50,
            "description": "Canned iced tea",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Bottled Water",
            "price": 2.00,
            "description": "500ml bottled water",
            "inStock": True,
            "allergens": ""
        },
        {
            "name": "Lemonade",
            "price": 3.00,
            "description": "Fresh lemonade",
            "inStock": True,
            "allergens": ""
        },
        
        # Combo Meals
        {
            "name": "Classic Combo",
            "price": 13.00,
            "description": "Any hot dog with fries and a drink",
            "inStock": True,
            "allergens": "gluten"
        },
        {
            "name": "Deluxe Combo",
            "price": 16.00,
            "description": "Any premium hot dog with poutine and a drink",
            "inStock": True,
            "allergens": "gluten, lactose"
        }
    ]
})


order.insert_one({
    "building": "210",
    "room": "115",
    "subTotal": 13.50, 
    "orderStatus": "Complete",
    "orderTime": 1100,           #  Integer format: HHMM (11:00 AM)
    "readyTime": 1107,           #  11:07 AM
    "acceptTime": 1107,          #  11:07 AM
    "deliveryTime": 1115,        #  11:15 AM
    "pickupTime": 1110,          #  11:10 AM
    "agent": "Kyle",
    "vendor": "Upper Cafe",
    "cartItem": [                
        {
            "name": "Chicken Strips",
            "qty": 1
        },
        {
            "name": "Coffee",
            "qty": 1
        }
    ]
})
client.close()

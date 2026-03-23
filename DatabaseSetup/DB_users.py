def insert_all_users(user):
	# Clear database to avoid duplicates
	filter_users = {
		"name": {
			"$in": ["Lower Cafeteria", "Upper Cafeteria", "Unleashed Hot Dogs",  # Vendors
					"Dr. Sarah Elizabeth Carruthers", "Caleb Bronn", "Keenan Wolfe",  # Customers
					"Emily Chen", "Marcus Johnson", "Sarah Martinez", "David Lee",
					"Priya Patel", "Alex Thompson", "Jessica Wang",
					"Bruce Fernandes", "Surya Balram", "Mike Stevens", "Jennifer Lopez",  # Agents
					"Robert Kim", "Amanda Wilson", "Carlos Rodriguez", "Lisa Zhang"]
		}
	}
	user.delete_many(filter_users)

	# Vendors
	lower_caf = {
		"name": "Lower Cafeteria",
		"email": "foodservices@viu.ca",
		"VIUID": "000000001",
		"role": "Vendor",
		"active": True,
		"location": "Building 185 Cafeteria",
		"hoursOfOperation": {
			"days": "Mon-Fri",
			"startTime": "07:30",
			"endTime": "14:00",
		}
	}

	upper_caf = {
		"name": "Upper Cafeteria",
		"email": "foodservices@viu.ca",
		"VIUID": "000000002",
		"role": "Vendor",
		"active": True,
		"location": "Building 300 Cafeteria",
		"hoursOfOperation": {
			"days": "Mon-Fri",
			"startTime": "07:30",
			"endTime": "19:00",
		}
	}

	unleashed_hot_dogs = {
		"name": "Unleashed Hot Dogs",
		"email": "unleashedhotdogs@gmail.com",	# made-up email 'cos the hot dog guy doesn't have one (that I can find)
		"VIUID": "000000003",
		"role": "Vendor",
		"active": True,
		"location": "Royal Bank Plaza",
		"hoursOfOperation": {
			"days": "Tue-Thu",
			"startTime": "11:00",
			"endTime": "15:00",
		}
	}

	user.insert_many([lower_caf, upper_caf, unleashed_hot_dogs])
	print("Vendors inserted into the database")

	# Customers
	dr_sarah = {
		"name": "Dr. Sarah Elizabeth Carruthers",
		"email": "sarah.carruthers@iu.ca",
		"VIUID": "100000000",
		"role": "Customer",
		"active": True,
		"previouslyOrdered": [],
	}

	keenan = {
		"name": "Caleb Bronn",
		"email": "brick.cuppy@gmail.com",
		"VIUID": "633377721",
		"role": "Customer",
		"active": True,
		"previouslyOrdered": [],
	}

	caleb = {
		"name": "Keenan Wolfe",
		"email": "Paniniwolfe@gmail.com",
		"VIUID": "666742069",
		"role": "Customer",
		"active": True,
		"previouslyOrdered": [],
	}

	kyle = {
        "name": "Kyle",
        "email": "losermgee@viu.ca",
        "role": "Customer",
        "VIUID": "123456789",
		"active": True,
        "previouslyOrdered": [
            "Chicken Strips", "Coffee", "Monster", "Hot Dog"
        ]
    }

	emily = {
        "name": "Emily Chen",
        "email": "emily.chen@viu.ca",
        "role": "Customer",
        "VIUID": "456789123",
		"active": True,
        "previouslyOrdered": [
            "Caesar Salad", "Latte", "Blueberry Muffin", "Greek Salad"
        ]
    }

	marcus = {
        "name": "Marcus Johnson",
        "email": "mjohnson@gmail.com",
        "role": "Customer",
        "VIUID": "789123456",
		"active": True,
        "previouslyOrdered": [
            "Pepperoni Pizza", "Coke", "Chicken Wings"
        ]
    }

	martinez = {
        "name": "Sarah Martinez",
        "email": "sarah.m@viu.ca",
        "role": "Customer",
        "VIUID": "321654987",
		"active": True,
        "previouslyOrdered": [
            "Veggie Burger", "Iced Tea", "Fresh Fruit Cup", "Yogurt Parfait"
        ]
    }

	david = {
		"name": "David Lee",
		"email": "david.lee88@gmail.com",
		"role": "Customer",
		"VIUID": "987654321",
		"active": True,
		"previouslyOrdered": [
			"BLT", "Coffee", "Chocolate Chip Cookie"
		]
	}

	priya = {
		"name": "Priya Patel",
		"email": "priya.patel@viu.ca",
		"role": "Customer",
		"VIUID": "147258369",
		"active": True,
		"previouslyOrdered": [
			"Falafel Wrap", "Smoothie", "Granola Bar", "Banana Bread"
		]
	}
	
	alex = {
		"name": "Alex Thompson",
		"email": "athompson@gmail.com",
		"role": "Customer",
		"VIUID": "258369147",
		"active": False,
		"previouslyOrdered": []  # New Customer, no previous orders
	}
	
	jessica = {
		"name": "Jessica Wang",
		"email": "jwang@viu.ca",
		"role": "Customer",
		"VIUID": "369147258",
		"active": False,
		"previouslyOrdered": [
			"Sushi Roll", "Green Tea", "Miso Soup", "Edamame"
		]
	}

	user.insert_many([dr_sarah, keenan, caleb, kyle, emily, marcus, martinez, david, priya, alex, jessica])
	print("Customers inserted into the database")

	# Delivery Agents
	bruce = {
		"name": "Bruce Fernandes",
		"email": "Bruixisawesome@gmail.com",
		"VIUID": "777888999",
		"role": "Agent",
		"active": True,
		"availabilityStatus": False,
	}

	surya = {
		"name": "Surya Balram",
		"email": "suryasgotgame@hotmail.com",
		"VIUID": "123123123",
		"role": "Agent",
		"active": True,
		"availabilityStatus": True,
	}

	mike = {
		"name": "Mike Stevens",
		"email": "mike.stevens@viu.ca",
		"role": "Agent",
		"VIUID": "111222333",
		"active": True,
		"availabilityStatus": True,  # Currently available
		"previouslyOrdered": []
	}
	jennifer = {
		"name": "Jennifer Lopez",
		"email": "jlopez.Agent@viu.ca",
		"role": "Agent",
		"VIUID": "222333444",
		"active": True,
		"availabilityStatus": True,
		"previouslyOrdered": ["Coffee"]
	}
	robert = {
		"name": "Robert Kim",
		"email": "rkim.delivery@viu.ca",
		"role": "Agent",
		"VIUID": "333444555",
		"active": True,
		"availabilityStatus": False,  # Currently not available
		"previouslyOrdered": []
	}
	amanda = {
		"name": "Amanda Wilson",
		"email": "awilson.Agent@viu.ca",
		"role": "Agent",
		"VIUID": "444555666",
		"active": True,
		"availabilityStatus": True,
		"previouslyOrdered": ["Breakfast Burrito", "Coffee"]
	}
	carlos = {
		"name": "Carlos Rodriguez",
		"email": "carlos.r@viu.ca",
		"role": "Agent",
		"VIUID": "555666777",
		"active": True,
		"availabilityStatus": True,
		"previouslyOrdered": ["Pizza", "Monster"]
	}
	lisa = {
		"name": "Lisa Zhang",
		"email": "lzhang.delivery@viu.ca",
		"role": "Agent",
		"VIUID": "666777888",
		"active": False,
		"availabilityStatus": False,
		"previouslyOrdered": []
	}

	user.insert_many([bruce, surya, mike, jennifer, robert, amanda, carlos, lisa])
	print("Delivery Agents inserted into the database")
# end insert_all_users


# Prompt user for username and password only if they run this file as a script (not as a module).
if __name__ == "__main__":
	from pymongo import MongoClient as MangoClient  # will this work?
	import getpass

	username = input("Enter you Mango username: ")
	password = getpass.getpass("Enter your Mango password: ")
	uri = f"mongodb://{username}:{password}@studb-mongo.csci.viu.ca:27017/{username}_project?authSource=admin"
	client = MangoClient(uri)

	db = client.get_database(f"{username}_project")
	user = db.get_collection("user")

	insert_all_users(user)
	client.close()
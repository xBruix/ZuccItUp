from datetime import datetime

def insert_all_orders(order):
	order.insert_one({
		"building": "210",
		"room": "115",
		"subTotal": 13.50,
		"specialInstructions": "Leave outside door to classroom",
		"orderStatus": "Received",
		"orderTime": datetime(2026, 2, 27, 11, 0, 0),  # 11:00 AM
		"acceptTime": datetime(2026, 2, 27, 11, 5, 0),  # 11:07 AM
		"readyTime": datetime(2026, 2, 27, 11, 7, 0),  # 11:07 AM
		"pickupTime": datetime(2026, 2, 27, 11, 10, 0),  # 11:10 AM
		"deliveryTime": datetime(2026, 2, 27, 11, 15, 0),  # 11:15 AM
		"customer": "Kyle",
		"agent": "Surya Balram",
		"vendor": "Upper Cafeteria",
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

	order.insert_one({
		"building": "315",
		"room": "114",
		"subTotal": 10.00,
		"specialInstructions": "",
		"orderStatus": "Received",
		"orderTime": datetime(2026, 3, 19, 12, 7, 0),	# 12:07 AM
		"acceptTime": datetime(2026, 3, 19, 12, 8, 0),  # 12:08 AM
		"readyTime": datetime(2026, 3, 19, 12, 10, 0),  # 12:10 AM
		"pickupTime": datetime(2026, 3, 19, 12, 12, 0), # 12:12 AM
		"deliveryTime": datetime(2026, 3, 19, 12, 15, 0),  # 12:15 AM
		"customer": "Kyle",
		"agent": "Bruce Fernandes",
		"vendor": "Unleashed Hot Dogs",
		"cartItem": [
			{
				"name": "The Chicago Dog",
				"qty": 1
			}
		]
	})
	print("Orders inserted into the database")
# end  insert_all_orders


# Prompt user for username and password only if they run this file as a script (not as a module).
if __name__ == "__main__":
	from pymongo import MongoClient as MangoClient  # will this work?
	import getpass

	username = input("Enter you Mango username: ")
	password = getpass.getpass("Enter your Mango password: ")
	uri = f"mongodb://{username}:{password}@studb-mongo.csci.viu.ca:27017/{username}_project?authSource=admin"
	client = MangoClient(uri)

	db = client.get_database(f"{username}_project")
	order = db.get_collection("order")

	# Clear database to avoid duplicates
	filter_orders = {
		"deliveryTime": {
			"$in": [datetime(2026, 2, 27, 11, 15, 0),
					datetime(2026, 3, 19, 12, 15, 0)]
		}
	}
	order.delete_many(filter_orders)

	insert_all_orders(order)
	client.close()
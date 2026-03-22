from pymongo import MongoClient as MangoClient
import getpass
# Import other DB files
from DB_menu import insert_all_menus
from DB_order import insert_all_orders
from DB_users import insert_all_users

username = input("Enter you Mango username: ")
password = getpass.getpass("Enter your Mango password: ")
uri = f"mongodb://{username}:{password}@studb-mongo.csci.viu.ca:27017/{username}_project?authSource=admin"
client = MangoClient(uri)

db = client.get_database(f"{username}_project")

# Collections
menu = db.get_collection("menu")
order = db.get_collection("order")  
user = db.get_collection("user")

# Call functions from other DB files to insert everything into the database
insert_all_menus(menu)
insert_all_orders(order)
insert_all_users(user)

print("\n...\nDatabase setup complete!")
client.close()

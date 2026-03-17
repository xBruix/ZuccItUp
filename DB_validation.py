from pymongo import MongoClient as MangoClient	# will this work?
import getpass

name = input("Enter monogoDB username \n")

password = getpass.getpass("Enter your Mango password:\n> ")
uri = f"mongodb://"+ name + ":{password}@studb-mongo.csci.viu.ca:27017/"+ name + "_project?authSource=admin"
client = MangoClient(uri)

db = client.get_database( name + "_project")  

db.create_collection("user", validator={ 
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email", "role", "VIUID"],
        "properties": {
            "name": {
                "bsonType": "string"
            },

            "email": {
                "bsonType": "string",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            },

            "VIUID": {
                "bsonType": "string",  
                "minLength": 9,
                "maxLength": 9,
                "pattern": "^[0-9]{9}$"
            },

            "role": {
                "bsonType": "string",
                "enum": ["agent", "customer", "vendor"]  
            },

            "availibilityStatus": {
                "bsonType": "bool"
            },

            "previouslyOrdered": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "maxItems": 100
            },

            "location": {
                "bsonType": "string"
            },

            "schedule": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string" }}}}}
)

db.create_collection("menu", validator={ 
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["type", "publishStatus"],
        "properties": {
            "type": {
                "bsonType": "string",
                "enum": ["Breakfast", "Lunch", "Dinner", "General"]
            },

            "schedule": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                }
            },

            "publishStatus": {
                "bsonType": "bool"
            },

            "menuItem": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "properties": {
                        "name": {
                            "bsonType": "string"
                        },

                        "price": {
                            "bsonType": "double",
                            "minimum": 0,
                            "maximum": 100
                        },

                        "description": {
                            "bsonType": "string"
                        },

                        "inStock": {
                            "bsonType": "bool"
                        },

                        "allergens": {
                            "bsonType": "string" }}}}}}}
)

db.create_collection("order", validator={
     "$jsonSchema": {  
        "bsonType": "object",
        "required": [],
        "properties": {
            "building": {
                "bsonType": "string",
                "minimum": 100,
                "maximum": 500
            },

            "room": {
                "bsonType": "string",
                "minimum": 0,
                "maximum": 500
            },

            "specialInstructions": {
                "bsonType": "string",
            },

            "subTotal": {
                "bsonType": "double",
                "minimum": 0
            },

            "orderStatus": {
                "bsonType": "string"
            },

            "orderTime": {  
                "bsonType": "date",
                "description": "must be a valid ISO Date object"
            },

            "readyTime": { 
                "bsonType": "date",
                "description": "must be a valid ISO Date object"
            },

            "acceptTime": {  
                "bsonType": "date",
                "description": "must be a valid ISO Date object"
            },

            "deliveryTime": {  
                "bsonType": "date",
                "description": "must be a valid ISO Date object"
            },

            "pickupTime": { 
                "bsonType": "date",
                "description": "must be a valid ISO Date object"
            },

            "agent": {
                "bsonType": "string",
                "description": "Name of the agent assigned to order"
            },

            "vendor": {
                "bsonType": "string",
                "description": "Name of the Vendor order is from"
            },

            "customer": {
                "bsonType": "string",
                "description": "Name of the customer who placed the order"
            },

            "cartItem": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "properties": {
                        "name": {
                            "bsonType": "string"
                        },

                        "qty": {
                            "bsonType": "int" }}}}}}}
)
client.close()
from pymongo import MongoClient as MangoClient	# will this work?
import getpass

username = input("Enter you Mango username:\n> ")
password = getpass.getpass("Enter your Mango password:\n> ")
uri = f"mongodb://{username}:{password}@studb-mongo.csci.viu.ca:27017/{username}_project?authSource=admin"
client = MangoClient(uri)

db = client.get_database(username + "_project")

try:
    db.drop_collection("menu")
except:
    pass
try:
    db.drop_collection("user")
except:
    pass
try:
    db.drop_collection("order")
except:
    pass

db.create_collection("user", validator={ 
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email", "role", "VIUID"],
        "properties": {
            # REQUIRED for all user types
            "name": {
                "bsonType": "string"
            },
            # REQUIRED for all user types
            "email": {
                "bsonType": "string",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            },
            # REQUIRED for all user types
            "VIUID": {
                "bsonType": "string",  
                "minLength": 9,
                "maxLength": 9,
                "pattern": "^[0-9]{9}$"
            },
            # REQUIRED for all user types
            "role": {
                "bsonType": "string",
                "enum": ["agent", "customer", "vendor"]  
            },
            # Only used by Delivery Agent
            "availabilityStatus": {
                "bsonType": "bool"
            },
            # Only used by Customer
            "previouslyOrdered": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "maxItems": 100
            },
            # Only used by Vendor
            "location": {
                "bsonType": "string"
            },
            # Only used by Vendor
            "hoursOfOperation": {
                "bsonType": "object",
                "properties": {
                    "days": {
                        "bsonType": "string",
                        "pattern": "\\w\\w\w-\\w\\w\\w",     # Must be in 3-letter format like this: Mon-Fri
                    },
                    "startTime": {
                        "bsonType": "string",
                        # Must be in 24-hour time with leading zeros, e.g. 23:59 or 07:30
                        "pattern": "([0-1][0-9]|2[0-3]):[0-5][0-9]",
                    },
                    "endTime": {
                        "bsonType": "string",
                        # Must be in 24-hour time with leading zeros, e.g. 23:59 or 07:30
                        "pattern": "([0-1][0-9]|2[0-3]):[0-5][0-9]",
                    },
                }
            }}}}
)

db.create_collection("menu", validator={ 
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["type"],
        "properties": {
            "type": {
                "bsonType": "string",
                "enum": ["breakfast", "lunch", "dinner", "general"]
            },

            "schedule": {
                "bsonType": "object",
                "properties": {
                    "days": {
                        "bsonType": "string",
                        "pattern": "\w\w\w-\w\w\w",     # Must be in format like this: Mon-Fri
                    },
                    "startTime": {
                        "bsonType": "string",
                        # Must be in 24-hour time with leading zeros, e.g. 23:59 or 07:30
                        "pattern": "([0-1][0-9]|2[0-3]):[0-5][0-9]",
                    },
                    "endTime": {
                        "bsonType": "string",
                        # Must be in 24-hour time with leading zeros, e.g. 23:59 or 07:30
                        "pattern": "([0-1][0-9]|2[0-3]):[0-5][0-9]",
                    },
                }
            },

            # No longer necessary since we're not implementing the Vendor
            # "publishStatus": {
            #     "bsonType": "bool"
            # },

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
        "required": ["building", "room"],
        "properties": {
            "building": {
                "bsonType": "string",
                "pattern": "[1-4]\d\d"
            },

            "room": {
                "bsonType": "string",
                "pattern": "[1-5]\d\d\w?"
            },

            "specialInstructions": {
                "bsonType": "string",
            },

            "subTotal": {
                "bsonType": "double",
                "minimum": 0
            },

            "orderStatus": {
                "bsonType": "string",
                "enum": ["pending", "readyForPickup", "inTransit", "delivered", "received"]
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
                            "bsonType": "string",
                        },

                        "qty": {
                            "bsonType": "int",
                            "minimum": 0,
                        }}}}}}}
)

client.close()

print("Collections added:")
print("- Menu\n- Order\n- User")
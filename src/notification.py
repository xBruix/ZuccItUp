# Authors: Surya Balram, Bruce Fernandes

# This file defines the Notification class.
# It represents a notification that can be sent to users,
# including its time, description, and heading.
from datetime import datetime

STATUS_MESSAGES = {
    "Pending": (
        "Order Placed",
        "Your order from {vendor} has been placed and is waiting for a delivery agent.",
    ),
    "ReadyForPickup": (
        "Order Ready for Pickup",
        "Your order from {vendor} is packaged and ready to be picked up by a delivery agent.",
    ),
    "InTransit": (
        "Order On Its Way",
        "Your order from {vendor} has been accepted by {agent} and is on its way!",
    ),
    "Delivered": (
        "Order Delivered",
        "Your order from {vendor} has been delivered by {agent}. Please confirm receipt.",
    ),
    "Received": (
        "Order Confirmed",
        "Thank you! Your order from {vendor} has been confirmed as received.",
    ),
}                                                                       #this is to avoid db

class Notification():

    def __init__(self, heading: str, description: str, customer_VIUID: str, server, order_id: str = "",):


        
        self.time = datetime.now()
        self.description = description
        self.heading = heading
        self.customer_VIUID = str(customer_VIUID)                       #added this for tracking whice one is which
        self.order_id = str(order_id) if order_id else ""               #same with this
        self.server = server                                            #server instance for db interaction
    
    #i had to make a helper function so that notifications do not have a collection in the db
    def _build_message(self, order: dict) -> tuple[str, str]:
        
        status = order.get("orderStatus", "")                           #we get the notification based on the order status
        vendor = order.get("vendor", "the vendor")                      #the vendor name to display
        agent  = order.get("agent") or "your delivery agent"            #the agent assigned or we give the generic "your delivery agent"
 
        if status in STATUS_MESSAGES:                                   #sanity check to make sure it returns the status message as given at the top of this file
            heading, description_template = STATUS_MESSAGES[status]     #pulls from the messages at the top based on the status of the order
            description = description_template.format(vendor=vendor, agent=agent)
            return heading, description
 
        return self.heading, self.description                           #this is a fallback if the order status is just wrong
    
    def sendNotification(self):
        
        heading = self.heading
        description = self.description
        
        if self.order_id:
            order=self.server.get_order_by_id(self.order_id)            #getting order from db to find current status
            
            if order:
                heading, description = self._build_message(order)
        
        print(f"\n  [{self.time.strftime('%Y-%m-%d %H:%M')}]")          #time
        print(f"  {heading}")                                           #heading print
        print(f"  {description}")                                       #might not need to print the description
        print("  " + "─" * 50)                                          #divider line
        print(f"Notification sent to customer{self.customer_VIUID}")    #notification send
        return {"heading":heading,"description":description}            #since i now return the dictionary, the caller can use the message                                          #

    def viewNotification(self):
        
        orders = self.server.get_orders_by_user(self.customer_VIUID)    #reading all orders for that user
        if not orders:
            print("Orders not found, please make an order to be notified.")
            return[]                                                    #no orders, no notification
        
        notifications=[]                                                #initialising notification list
        
        print(f"\n{'='*55}")                                            #divder line
        print(f"  Order Notifications for customer {self.customer_VIUID}")  #message to customer
        print(f"\n{'='*55}")                                            #divder line
        
        for order in orders:                                            #iterating through all orders
            heading, description = self._build_message(order)           #running helper function for the notification
            
            order_time = (
                order.get("deliveryTime")
                or order.get("acceptTime")
                or order.get("orderTime")
                or self.time                                            #iterating through to get what the current notification is on
            )
            time_str = order_time.strftime("%Y-%m-%d %H:%M") if order_time else "Unknown time"
                                                                        #this line does a few things
                                                                        #it converts the datetime string to readable string strftime converts it to the YYYY-MM-DD HH-MM-SS i omitted the seconds
                                                                        #so if the ordertime is not there, it will just display "unknown time"
            
            print(f"\n  [{time_str}]  Status: {order.get('orderStatus', 'Unknown')}")
            print(f"  {heading}")
            print(f"{description}")                                     #printing the heading and description, again we might not need description everytime
            
            if order.get("_id"):                                        #getting order id, if it does then prints the id
                print(f" Order ID: {order['_id']}")
            print(" "+ "─" * 50)                                        #divider line
            
            notifications.append({"heading": heading, "description": description, "order" : order}) #adds the dictionary to the notifications and then goes back to the for loop
            
        return notifications                                            #returning the list of notification as a dictionary
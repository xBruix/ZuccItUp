class Notification():
    def __init__(self, heading: str, description: str, customer_VIUID: str, order_id: str = ""):
        
        self.time = datetime.now()
        self.description =description
        self.heading = heading
        self.customer_VIUID = str(customer_VIUID)                       #added this for tracking whice one is which
        self.order_id = str(order_id) if order_id else ""               #same with this

    def sendNotification(self):
       
       notification_doc = {
            "heading": self.heading,
            "description": self.description,
            "customerVIUID": self.customer_VIUID,
            "orderId": self.order_id,
            "time": self.time,
            "read": False,                                              # marks whether the customer has seen it
        }
       
       result = db.notification.insert_one(notification_doc)            #db notification pull
       print(f"Notification sent to customer{self.customer_VIUDIF}")    #notification send
       return result.inserted_id                                        #who it was sent to

    def viewNotification(self):
        
        notifications = list(
            db.notification.find(
                {"customerVIUID": self.customer_VIUID}                  #pulling every notification for the ID from the db
            ).sort("time", -1)                                          # -1 = descending (newest first)
        )
 
        if not notifications:
            print("No notifications found.")                            #cant view something that dont exist
            return []
 
        print(f"\n{'═' * 55}")                                          #spacing and divider
        print(f"  Notifications for customer {self.customer_VIUID}")    #notifications
        print(f"{'═' * 55}")                                            #divider
 
        for n in notifications:                                         #iteration through the notifications
            time_str = n.get("time").strftime("%Y-%m-%d %H:%M") if n.get("time") else "Unknown time"
            read_str = "Read" if n.get("read") else "Unread"            #read or unread status
            print(f"\n  [{time_str}]  {read_str}")
            print(f"  {n.get('heading', '')}")
            print(f"  {n.get('description', '')}")                      #printing the notification
            if n.get("orderId"):
                print(f"  Order ID: {n.get('orderId')}")
            print("  " + "─" * 50)                                      #last divider
 
            # Mark the notification as read now that the customer has seen it
            db.notification.update_one(
                {"_id": n["_id"]},
                {"$set": {"read": True}}
            )                                                           #updating all to read since the notification is sent
 
        return notifications                                            #returning the list of notifications
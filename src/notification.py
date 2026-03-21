# Authors: Surya Balram

# This file defines the Notification class.
# It represents a notification that can be sent to users,
# including its time, description, and heading.

class Notification():
    # Constructor for Notification
    # Initializes the time, description, and heading of the notification
    def __init__(self, time: int, description: str, heading: str):
        
        self.time = time
        self.description =description
        self.heading = heading

    # Sends the notification to the intended recipient(s)
    # This method should handle the logic for delivering notifications
    def sendNotification(self):
        pass

    # Returns or displays the details of the notification
    # This can be used to view notification content
    def viewNotification(self):
        pass
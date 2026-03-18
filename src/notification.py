class Notification():
    def __init__(self, time: int, description: str, heading: str):
        
        self.time = time
        self.description =description
        self.heading = heading

    def sendNotification(self):
       pass

    def viewNotification(self):
        print("─" * 55)
        print("Here is your notification from monogodb")
        print("Here is your notification from mangodb")
        print("─" * 55)
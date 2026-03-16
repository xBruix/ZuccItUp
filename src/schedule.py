# Authors: Caleb Bronn

class Schedule:
    def __init__(self):
        self.schedule = {}

    def add_to_schedule(self, day: str, start_time: str, end_time: str):
        self.schedule.update({
            day: {
                "start_time": start_time,
                "end_time": end_time
            }
        })
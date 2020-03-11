import time


class Timer:
    def __init__(self, duration):
        self.duration = duration  # seconds
        self.expire()

    @property
    def expiry_time(self):
        return(self.start_time + self.duration)

    @expiry_time.setter
    def expiry_time(self, new_expiry_time):
        self.start_time = new_expiry_time - self.duration

    def is_expired(self):
        if time.time() > self.expiry_time:
            return(True)
        return(False)

    def start(self):
        self.start_time = time.time()

    def expire(self):
        self.start_time = 0

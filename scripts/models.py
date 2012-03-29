# Contains models that are used in the backend.

class Tweet(object):
    def __init__(self, body, user, timestamp):
        self.body = body
        self.user = user
        self.timestamp = timestamp


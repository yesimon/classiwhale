from abc import ABCMeta

"""Contains facilities for filtering tweets per user. A filter is an object
that takes the whole database as an input, and then returns, for a tweet and a
user, whether the tweet should be displayed to the user."""

class Filter(object):
    """ABC class for all objects that filter tweeds for a user."""
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def classify(self, user, tweet):
        raise NotImplemented


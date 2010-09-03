# Contains the an interface for accessing data from a database. Contains
#  implementations for sqlite at the moment.

from abc import ABCMeta, abstractmethod
from models import *

class ModelRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getTweetById(self, id):
        return None

    @abstractmethod
    def getTweetsByUser(self, user):
        return None

    @abstractmethod
    def getAllTweets(self):
        return None

    @abstractmethod
    def getUserById(self, id):
        return None

    @abstractmethod
    def getUsersForTweetId(self, id):
        return None

    @abstractmethod
    def getAllUsers(self):
        return None

class StatsRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def setCompatibility(self, u1, u2, score):
        pass

    @abstractmethod
    def setTweetScoreForUser(self, user, tweet, score):
        pass


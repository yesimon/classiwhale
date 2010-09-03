# Basic similarity matching, to determine which to follow, with a couple of
#  key modifications:
#   - Clustering - users are clustered in one of N groups (N determined
#       dynamically) based on which tweets they have rated or viewed
#   - Discounting - tweets that are older have less influence on the filtering
#       algorithm. This also applies to clustering.
#   - Matching - each user's preferences is a collection of tweets that they
#       have rated. For every other user in the universe (or in their cluster),
#       their compatibility score is (x - y) / z, where x is the number of
#       tweets the both users have agreed in rating, y is the number of tweets
#       where the users have disagreed in rating, and z is the number of tweets
#       in the universe (in the core cluster of tweets rated by these people).

import unittest
from models import Tweet

class Filter(object):

    def __init__(self, cluster = False, 
                       discount = True, 
                       up_multiplier = 1,
                       down_multiplier = 1,
                       threshold = 0): 
        self.tweets = set() # tweets ::= set<(body, user, timestamp)>
        self.users = { }    # users ::= map<name, map<tweetName, rating>>
        self.learned = False
        self.cluster = cluster # doesn't do anything right now
        self.discount = discount
        self.up = up_multiplier
        self.down = down_multiplier
        self.threshold = threshold

    def addUser(self, user):
        if user in self.users:
            raise NotImplemented, \
                "user {0} already identified in {1}".format(user, self)
        self.users[user] = { }

    def addTweet(self, user, tweet, rating):
        if user not in self.users or \
           rating not in [True, False]:
            raise NotImplemented, "user {0} does not exist".format(user)
        self.learned = False
        self.users[user][tweet] = rating
        self.tweets.add(tweet)
    
    def learn(self):
        self.com = { }
        users = self.users
        for user in users:
            self.com[user] = { }
            for user2 in users:
                if user2 != user:
                    self.com[user][user2] = self._cc(user, user2)
        self.learned = True

    def predict(self, user, tweet, forcePredict=False):
        if user not in self.users or \
           tweet not in self.tweets or \
           not self.learned:
            raise NotImplemented
        if tweet in self.users[user] and not forcePredict:
            rating = self.users[user][tweet]
            return (rating, float('+Inf') if rating else float('-Inf'))
        total = 0
        for u in self.users:
            if u != user:
                if tweet not in self.users[u]:
                    multiplier = 0
                elif self.users[u][tweet]:
                    multiplier = 1
                else:
                    multiplier = -1
                total += self.com[user][u] * multiplier
        return (total >= self.threshold, total)

    def _cc(self, user, user2):
        u = self.users
        tic = set(u[user].keys()) & set(u[user2].keys())
        ntwar = len([t for t in tic if u[user][t] == u[user2][t]])
        aggscore = self.up * ntwar - self.down * (len(tic) - ntwar)
        return float(aggscore) / len(self.tweets)

class FilterTest(unittest.TestCase):
    def test_learn_defaultArgs(self):
        # joe and bob match on everything, joe and mary disagree on everything.
        t = [ Tweet("joe and bob like this", 'shaq', 123),
              Tweet("joe and bob also like this", 'cr', 234),
              Tweet("joe and bob like this too", 'bob', 124),
              Tweet("joe likes this; bob doesn't", 'joe', 342),
              Tweet("joe likes this; mary doesn't", 'm', 534),
              Tweet("mary likes this; joe doesn't", 'df', 432),
              Tweet("all three dislike this one", 'sf', 342), ]

        filter = Filter()
        
        filter.addUser('joe')
        filter.addUser('bob')
        filter.addUser('mary')

        filter.addTweet('joe', t[0], True);
        filter.addTweet('joe', t[1], True);
        filter.addTweet('joe', t[2], True);
        filter.addTweet('joe', t[3], True);
        filter.addTweet('joe', t[4], True);
        filter.addTweet('joe', t[5], False);
        filter.addTweet('joe', t[6], False);

        filter.addTweet('bob', t[0], True);
        filter.addTweet('bob', t[1], True);
        filter.addTweet('bob', t[2], True);
        filter.addTweet('bob', t[3], False);
        filter.addTweet('bob', t[6], False);

        filter.addTweet('mary', t[4], False);
        filter.addTweet('mary', t[5], True);
        filter.addTweet('mary', t[6], False);

        filter.learn()

        self.assertEqual(filter.predict('bob', t[5]), (False, -2.0/7))
        self.assertEqual(filter.predict('mary', t[0]), (True, -0.0/7))
        self.assertEqual(filter.predict('joe', t[6]), (False, float('-Inf')))

if __name__ == '__main__':
    unittest.main()

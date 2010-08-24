import re
from argparse import ArgumentParser

parser = ArgumentParser(description="the thingy that does the doodad")
parser.add_argument('--test', dest='testFile', type=file,
                    help='Test data')
parser.add_argument('--train', dest='trainFile', type=file,
                    help='Training set')

NOT_RATED = '-'
RATED_UP = 'o'
RATED_DOWN = 'x'

CHAR_TO_RATING = {NOT_RATED : None, RATED_UP : True, RATED_DOWN : False}

class User(object):
    def __init__(self, id):
        self.id = id
        self.ratings = { }
        self.compat = { }
    def addTweet(self, tweet, direction):
        self.ratings[tweet] = direction
    def computeCompatibility(self, other):
        if not isinstance(other, User):
            raise NotImplemented
        total = len(set(self.ratings.keys()) & set(other.ratings.keys()))
        if total == 0:
            self._storeCompat(other, 0)
        else:
            spread = 0
            for key in set(self.ratings.keys()) & set(other.ratings.keys()):
                if self.ratings[key] == other.ratings[key]:
                    spread += 1
                else:
                    spread -= 1
            self._storeCompat(other, spread / total)
            
    def _storeCompat(self, other, val):
        other.compat[self] = val
        self.compat[other] = val

class Tweet(object):
    def __init__(self, id):
        self.id = id

if __name__ == '__main__':
    args = parser.parse_args()
    metadata = args.trainFile.readline()
    trainNumTweets, trainNumUsers = map(int, re.findall('[+-]?\d+', metadata))
    users = [User(id) for id in range(trainNumUsers)]
    tweets = [Tweet(id) for id in range(trainNumTweets)]
    
    tweetno = 0
    for line in args.trainFile:
        tweet = line.strip()
        for id in range(len(tweet)):
            if tweet[id] == RATED_UP:
                users[id].addTweet(tweets[tweetno], True)
            elif tweet[id] == RATED_DOWN:
                users[id].addTweet(tweets[tweetno], False)
        tweetno += 1


    # compute compatibilities
    for i in xrange(len(users)):
        for j in xrange(i, len(users)):
            users[i].computeCompatibility(users[j])
    
    metadata = args.testFile.readline()
    testNumTweets, testNumUsers = map(int, re.findall('[+-]?\d+', metadata))
    for i in range(testNumTweets):
        tweet = args.testFile.readline().strip()
        print "Tweet {0}: {1}".format(i, tweet)
        
        tweetProfile = [CHAR_TO_RATING[x] for x in  tweet]
        for id in range(len(tweetProfile)):
            if tweetProfile[id] is None:
                sum = 0
                for j in range(len(tweetProfile)):
                    if tweetProfile[j] == True:
                        m = 1
                    elif tweetProfile[j] == False:
                        m = -1
                    else:
                        m = 0
                    sum += users[id].compat[users[j]] * m
                print "  User {0} - score: {1} - rating: {2}".format(
                    id, sum, "up" if sum >= 0 else "down")


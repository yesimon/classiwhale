from django.core.management import setup_environ
import sys
sys.path.append('../dxm/')


# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)
CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')

############ Script ##############

import twitter
import pickle
from datetime import datetime
import time
from status.models import Status
from twitterauth.models import UserProfile, Rating



tweeters = ['nytimes', 'TheEconomist', 'russellcrowe', 'sn00ki', 'BarackObama', 
    'Stanford', 'QueenRania', 'StephenAtHome', 'NASA', 'ladygaga', 'Oprah',
    'FT', 'taylorswift13', 'jtimberlake', 'justinbieber', 'katyperry', 'cnnbrk',
    'twitter', 'TheOnion', 'coldplay', 'PerezHilton', 'google', 'THE_REAL_SHAQ',
    'MariahCarey']
    


d = datetime(2010, 9, 25, 0, 0, 0)
since_date = d.isoformat()


        
class Container:
    
    def __init__(self, dictionary):
        self.__dict__ = dictionary
        
def GetTweets(file, USERS=None, COUNT_DEFAULT=50, COUNT={}):
    """
    COUNT_DEFAULT is the default number of tweets to get for each
    user, which falls back on 50. COUNT is a dictionary with with keys
    as tweeters and value the number of tweets to get. Falls back on 
    COUNT_DEFAULT
    """
    api = twitter.Api()
    t = {'statuses': {}, 'users': {}}
    for u in USERS:
        try: n = COUNT[u]
        except: n = COUNT_DEFAULT
        try: 
            user=api.GetUser(u)
            timeline = api.GetUserTimeline(id=u, count=n)
            t['users'][user.id] = user
            t['statuses'][user.id] = timeline
        except: 
            print "User: '{0}' has protected tweets".format(u)
    pickle.dump(t, file)




def main():
    import argparse
    parser = argparse.ArgumentParser(description='Grab tweets/users from twitter to store locally in a pickled file.')
    parser.add_argument("--get", nargs='?', type=argparse.FileType('w'),
        const='tweets.pkl', default=False, dest="GET")
    parser.add_argument("--create", nargs='?', type=argparse.FileType('r'),
        const='train_set.pkl', default=False, dest="CREATE")
    ARGS = parser.parse_args()

    import import_tweets_settings
    



    if ARGS.GET:
        GetTweets(ARGS.GET, **import_tweets_settings.__dict__)
        
    if ARGS.CREATE:
        pass

#        CreateTrainingSet(ARGS.CREATE)

    
    
    
    

if __name__ == '__main__':
    main()

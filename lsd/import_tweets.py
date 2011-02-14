from django.core.management import setup_environ
import sys
sys.path.append('../dxm/')


# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)
CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')
RATER_PASSWORD = 'testtest'

############ Script ##############

import pickle
import itertools
from datetime import datetime
from email.utils import parsedate
from time import mktime
from django.db import transaction
from django.contrib.auth.models import User
from twython import Twython

from twitter.models import *






        
class Container:
    
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)
        
def GetTweets(file, USERS=None, COUNT_DEFAULT=50, COUNT={}, **kwargs):
    """
    COUNT_DEFAULT is the default number of tweets to get for each
    user, which falls back on 50. COUNT is a dictionary with with keys
    as tweeters and value the number of tweets to get. Falls back on 
    COUNT_DEFAULT
    """
    api = Twython()
    t = {'statuses': {}, 'users': {}}
    for u in USERS:
        try: n = COUNT[u]
        except: n = COUNT_DEFAULT
        try: 
            user=api.showUser(u)
            timeline = api.getUserTimeline(id=u, count=n)
            t['users'][user['id']] = user
            t['statuses'][user['id']] = timeline
        except: 
            print "User: '{0}' has protected tweets".format(u)
    pickle.dump(t, file)

def FullCreateUser(user, fake=False):
    """Full create user/userprofile from api user object"""
    tp = TwitterUserProfile.construct_from_dict(user)
    tp.save()
    return tp
"""
    u, created = User.objects.get_or_create(id=user.id, username=user.id)
    if created: 
        if fake: u.set_password(RATER_PASSWORD)
        else: u.set_unusable_password()
        u.first_name=user.name
        u.save()
    p, created = UserProfile.objects.get_or_create(user=u)
    if (created or
    p.screen_name != user.screen_name or
    p.profile_image_url != user.url or
    p.location != user.location or
    p.url != user.url or
    p.description != user.description):  
        p.screen_name = user.screen_name
        p.profile_image_url = user.profile_image_url
        p.location = user.location
        p.url = user.url
        p.description = user.description
        p.save()
    return u, p
"""
    
    
def CreateStatus(status):
    """Full create status from python dict status. Guarantee
    foreignkey references exist in database"""
    status = Status.construct_from_dict(status)
    return s


def AddStatuses(statuses):
    """Adds and returns full set of statuses (ids) stored in t as django Status 
    model instances
    """
    s_ids = [s['id'] for s in statuses]
    s_found = Status.objects.in_bulk(s_ids)
    status_set = s_found.values()
    s_toadd = [s for s in statuses if s['id'] not in 
               [sid for sid in s_found]]
    status_create_set = map(CreateStatus, s_toadd)
    save_instances(status_create_set)
#    for s in status_create_set:
#        s.save()
    status_set.extend(status_create_set)
    return status_set


    
@transaction.commit_on_success
def save_instances(instances):
    """Note transactions only work for InnoDB on MySQL"""
    for inst in instances:
        inst.save()
        
@transaction.commit_on_success
def add_m2m_instances(forward, instances):
    """Note transactions only work for InnoDB on MySQL"""
    for inst in instances:
        forward.add(inst)
            

def InsertData(file):
    """Inserts users and tweets as specified by file"""
    try: t = pickle.load(file)
    except:
        print "Error unpickling file '{0}'".format(file.name)
        sys.exit()
    statuses, users = t['statuses'], t['users']
    # Create all missing tweeters from training set
    model_users = map(FullCreateUser, users.values())
    # Create all missing statuses from training set
    model_statuses = itertools.chain(map(AddStatuses, statuses.values()))





def main():
    import argparse
    parser = argparse.ArgumentParser(description='Grab tweets/users from twitter to store locally in a pickled file.')
    parser.add_argument("--get", nargs='?', type=argparse.FileType('w'),
        const='tweets.pkl', default=False, dest="GET")
    parser.add_argument("--create", nargs='?', type=argparse.FileType('r'),
        const='tweets.pkl', default=False, dest="CREATE")
    ARGS = parser.parse_args()

    import import_tweets_settings
    
    
    if ARGS.GET:
        GetTweets(ARGS.GET, **import_tweets_settings.__dict__)
        
    if ARGS.CREATE:
        InsertData(ARGS.CREATE)

    
    
    
    

if __name__ == '__main__':
    main()

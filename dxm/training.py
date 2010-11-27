from django.core.management import setup_environ
import sys

# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)

############ Script ##############

import twitter
import pickle
import random
import copy
from datetime import datetime
import time
from django.db import transaction
from django.contrib.auth.models import User
from status.models import Status
from twitterauth.models import UserProfile, Rating


CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')

tweeters = ['nytimes', 'TheEconomist', 'russellcrowe', 'sn00ki', 'BarackObama', 
    'Stanford', 'QueenRania', 'StephenAtHome', 'NASA', 'ladygaga', 'Oprah',
    'FT', 'taylorswift13', 'jtimberlake', 'justinbieber', 'katyperry', 'cnnbrk',
    'twitter', 'TheOnion', 'coldplay', 'PerezHilton', 'google', 'THE_REAL_SHAQ',
    'MariahCarey']
    
# Banned raters
#raters = ['classiwhale0{0}'.format(i) for i in range(10)]
#raters.extend(['classiwhale{0}'.format(i) for i in range(10, 25)])

# New raters - not actual twitter accounts
raters = [i for i in range(100, 125)]
RATER_PASSWORD = 'testtest'

d = datetime(2010, 9, 25, 0, 0, 0)
since_date = d.isoformat()

alpha = 0.5 # Percentage of tweeters for each rater to follow


class TrainingSet:

    def __init__(self):
        self.tweetdb = {}
        self.tweeters = {}
        self.raters = {}

class TrainingUser:

    def __init__(self, id):
        self.id = id
        self.screen_name = 'classiwhale{0}'.format(id)
        self.name = 'Test {0}'.format(id)
        self.profile_image_url = None
        self.location = None
        self.url = None
        self.description = None
        
        
def GetTweets(file, tweeters, raters):
    api = twitter.Api()
    train_set = TrainingSet()
    for tweeter in tweeters:
        try: timeline = api.GetUserTimeline(id=tweeter, count=50)
        except: 
            print "User: '{0}' has protected tweets".format(tweeter)
        train_set.tweetdb[tweeter] = timeline
        try: user = api.GetUser(tweeter)
        except: print "Cannot get user '{0}'".format(tweeter)
        train_set.tweeters[tweeter] = user
    for rater in raters:
        #try: user = api.GetUser(rater)
        try: user = TrainingUser(rater)
        except:
            print "Cannot get user '{0}'".format(rater)
            sys.exit()
        train_set.raters[rater] = user 
    pickle.dump(train_set, file)

def FullCreateUser(user):
    """Full create user/userprofile from api user object"""
    u, created = User.objects.get_or_create(id=user.id, username=user.id)
    if created: 
        #u.set_unusable_password()
        u.password=RATER_PASSWORD
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
    
    
    
def FullCreateStatus(status):
    """Full create status from api status object. Does not guarantee
    foreignkey references exist in database"""
    from email.utils import parsedate
    from time import mktime
    created_at = datetime.fromtimestamp(mktime(parsedate(status.created_at)))
    content_length = len(status.text)
    s = Status(
                id = status.id,
                text = status.text,
                created_at = created_at,
                content_length= content_length,
               )
    s.author_id = status.user.id
    s.in_reply_to_user_id = status.in_reply_to_user_id
    s.in_reply_to_status_id = status.in_reply_to_status_id  
    return s

def AddStatuses(statuses):
    """Adds and returns full set of statuses in statuses as django Status 
    model instances
    """
    s_ids = [s.GetId() for s in statuses]
    s_found = Status.objects.in_bulk(s_ids)
    status_set = s_found.values()
    s_found_ids = [s_found[s].id for s in s_found]
    s_toadd_ids = set(s_ids)-set(s_found_ids)
    s_toadd = [s for s in statuses if s.id in s_toadd_ids]
    status_create_set = []
    for status in s_toadd:
        s = FullCreateStatus(status)
        status_create_set.append(s)
    save_instances(status_create_set)
#    for s in status_create_set:
#        s.save()
    status_set.extend(status_create_set)
    return status_set

def AddTrainingStatuses(profile, api_statuses, model_statuses):
    """Adds training statuses to profile"""
    s_ids = [s.GetId() for s in api_statuses]
    ts_found = profile.training_statuses.all()
    ts_found_ids = [s.id for s in ts_found]
    ts_toadd_ids = set(s_ids)-set(ts_found_ids)
    print ts_toadd_ids
    ts_toadd = [s for s in model_statuses if (s.id in ts_toadd_ids)]
    add_m2m_instances(profile.training_statuses, ts_toadd)

#    for s in ts_toadd:
#        profile.training_statuses.add(s)
    
    
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
            

def CreateTrainingSet(file):
    try: train_set = pickle.load(file)
    except:
        print "Error unpickling file '{0}'".format(file.name)
        sys.exit()
    (tweetdb, raters) = (train_set.tweetdb, train_set.raters)
    # Create all missing tweeters from training set
    for tweeter in train_set.tweeters:
        FullCreateUser(train_set.tweeters[tweeter])
    # Create all missing statuses from training set
    api_statuses = []
    map(api_statuses.extend, train_set.tweetdb.values())
    model_statuses = AddStatuses(api_statuses)
    tweeters = tweetdb.keys()
    num_tweeters = len(tweeters)
    random.seed()
    for rater in raters:
        print "Creating training set for '{0}'".format(rater)
        user, profile = FullCreateUser(raters[rater])
        status_sample = []
        tweeter_sample = random.sample(tweeters, int(num_tweeters*alpha))
        for tweeter in tweeter_sample:
            status_sample.extend(tweetdb[tweeter])
        AddTrainingStatuses(profile, status_sample, model_statuses)

                    

def DumpRatings(file):
    ratingdb = {}
    users = UserProfile.objects.filter(screen_name__in=raters)
    for user in users:
        ratingdb[user.screen_name] = {}
        ratings = Rating.objects.filter(user_profile=user)
        for rating in ratings:
            ratingdb[user.screen_name][rating.status_id] = rating
    pickle.dump(ratingdb, file)
    


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create classiwhale training set for human ratings.')
    parser.add_argument("--get", nargs='?', type=argparse.FileType('w'),
        const='train_set.pkl', default=False, dest="GET")
    parser.add_argument("--create", nargs='?', type=argparse.FileType('r'),
        const='train_set.pkl', default=False, dest="CREATE")
    parser.add_argument("--dump", nargs='?', type=argparse.FileType('w'), 
        const='train_set_dump.pkl', default=False, dest="DUMP")
    ARGS = parser.parse_args()
    
    if ARGS.GET:
        GetTweets(ARGS.GET, tweeters, raters)
        
    if ARGS.CREATE:
        CreateTrainingSet(ARGS.CREATE)

    if ARGS.DUMP:
        DumpRatings(ARGS.DUMP)




    
    
    
    

if __name__ == '__main__':
    main()
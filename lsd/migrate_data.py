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

#from twitterauth.models import UserProfile as OldTwitterUserProfile
#from status.models import Status as OldStatus
#from twitterauth.models import Rating as OldRating

from twitter.models import *

def MigrateUserProfiles():
    old_profs = OldTwitterUserProfile.objects.all()
    for prof in old_profs:
        print("Migrating user profile {0}".format(prof.user_id))
        setattr(prof, 'id', prof.user_id)
        field_dict = {}
        for field in TwitterUserProfile.available_fields:
            try: field_dict[str(field)] = getattr(prof, field)
            except AttributeError: pass
        tp = TwitterUserProfile(**field_dict)
        tp.save()

def FixUserProfiles():
    users = User.objects.all()
    for u in users:
        try: 
            twitter_id = int(u.username.split('@')[0])
            prof = UserProfile.objects.get(user=u)
        except: continue
        print("Fixing user {0} {1}".format(u.first_name, u.last_name))
        tp = TwitterUserProfile.objects.get(id=twitter_id)

        tp.user = prof
        tp.active_classifier = 'CylonBayesClassifier'
        tp.classifier_version = '0.1'
        tp.save(override=True)


def MigrateStatuses():
    old_statuses = OldStatus.objects.all()
    new_statuses_ids = set([s.id for s in Status.objects.all()])
    old_statuses = [s for s in old_statuses if s.id not in new_statuses_ids]
    for status in old_statuses:
        setattr(status, 'user', status.user_profile_id)
        field_dict = {}
        for field in Status.available_fields:
            try: field_dict[str(field)] = getattr(status, field)
            except AttributeError: pass
        field_dict['user_id'] = field_dict['user']
        del field_dict['user']
        s = Status(**field_dict)
        try: Status.objects.get(id=s.id)
        except:
            print("Migrating status {0}".format(status.id))
            s.save()

def MigrateRatings():
    old_ratings = OldRating.objects.all()
    for rating in old_ratings:
        print("Migrating rating {0}".format(rating.id))
        r = Rating(user_id=rating.user_profile_id,
                   status_id=rating.status_id,
                   rating=rating.rating,
                   rated_time=rating.rated_time)
        r.save()

if __name__ == "__main__":
    FixUserProfiles()

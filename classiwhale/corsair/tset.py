######## Django Environment Setup #######

from django.core.management import setup_environ
import sys
# horrific path mangling here :(
sys.path.extend(['../', '../../lib/'])

import settings
setup_environ(settings)

######## Script Begin #######

from twitter.models import *
from corsair.models import TwitterTrainingSet

twitteruserprofile_ids = [str(i) for i in range(100, 125)]

#twitteruserprofile_ids = [str(100)]

ratings = Rating.objects.filter(user__in=twitteruserprofile_ids)
twitter_user_profiles = TwitterUserProfile.objects.filter(pk__in=twitteruserprofile_ids)
name = 'CS229 Training Set'

#name = 'Mini Training Set'
try:
    t = TwitterTrainingSet.objects.get(name=name)
except:
    t = TwitterTrainingSet(name=name)
    t.save()
map(t.ratings.add, ratings)
map(t.users.add, twitter_user_profiles)
t.save()

######## Django Environment Setup #######

from django.core.management import setup_environ
import sys
# horrific path mangling here :(
sys.path.extend(['../../dxm/', '../', '../../lib/'])

# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)
    
######## Script Begin #######

from twitter.models import *
from corsair.models import TrainingSet

userprofile_ids = [str(i) for i in range(100, 125)]

userprofile_ids = [str(100)]

ratings = Rating.objects.filter(user__in=userprofile_ids)
user_profiles = TwitterUserProfile.objects.filter(pk__in=userprofile_ids)
name = 'CS229 Training Set'

name = 'Mini Training Set'
try:
    t = TrainingSet.objects.get(name=name)
except:
    t = TrainingSet(name=name)
    t.save()
map(t.ratings.add, ratings)
map(t.user_profiles.add, user_profiles)
t.save()

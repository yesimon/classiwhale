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

from twitterauth.models import UserProfile, Rating
from status.models import Status
from corsair.models import TrainingSet

userprofile_ids = [str(i) for i in range(100, 125)]

ratings = Rating.objects.filter(user_profile__in=userprofile_ids)
user_profiles = UserProfile.objects.filter(pk__in=userprofile_ids)
name = 'CS229 Training Set'

try:
    t = TrainingSet.objects.get(name=name)
except:
    t = TrainingSet(name=name)
    t.save()
map(t.ratings.add, ratings)
map(t.user_profiles.add, user_profiles)
t.save()

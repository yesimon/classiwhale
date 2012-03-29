from django.conf import settings
from twython import Twython

from twitter.models import TwitterUserProfile, Status

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')



def get_authorized_twython(authorized_tokens):
    api = Twython(
        twitter_token = CONSUMER_KEY,
        twitter_secret = CONSUMER_SECRET,
        oauth_token = authorized_tokens['oauth_token'],
        oauth_token_secret = authorized_tokens['oauth_token_secret']
    )
    return api

def full_create_status(status):
    status = Status.create_from_dict(status)
    try: TwitterUserProfile.objects.get(id=status.user.id)
    except TwitterUserProfile.DoesNotExist:
        status.user.save()
    try: Status.objects.get(id=status.id)
    except: status.save()
    return status

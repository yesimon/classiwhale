from django.conf import settings
from django.contrib.auth.models import User

from twython import Twython

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')

class TwitterAuthentication:
    """Twitter backend for authentication
    """
    supports_anonymous_user = False
    def authenticate(self, oauth_token=None, oauth_secret=None):
        '''
        Authenticates the oauth credentials by requesting user information
        from twitter.
        '''
        api = Twython(
            twitter_token = CONSUMER_KEY,
            twitter_secret = CONSUMER_SECRET,
            oauth_token = oauth_token,
            oauth_token_secret = oauth_secret
        )

        twitter_user = api.verifyCredentials()

        username = '@'.join([str(twitter_user['id']), 'twitter'])
        try:
            user = User.objects.get(username=username)
        except:
            # User wasn't been registered through this backend
            return None
        return user
        
    
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            return None

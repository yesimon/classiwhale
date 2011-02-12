
#!/usr/bin/env python
"""Twitter Authentication backend for Django

Requires:
AUTH_PROFILE_MODULE to be defined in settings.py

The profile models should have following fields:
        access_token
        url
        location
        description
        profile_image_url
        screen_name
"""

from django.conf import settings
from django.contrib.auth.models import User
from twitterauth.models import UserProfile
from whale.models import Whale, WhaleSpecies

import python_twitter

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')
DEFAULT_CLASSIFIER = 'CylonBayesClassifier'
DEFAULT_CLASSIFIER_VERSION = '0.1'


class TwitterBackend:
    """TwitterBackend for authentication
    """
    def authenticate(self, access_token):
        '''authenticates the token by requesting user information from twitter
        '''
        twitter_api = python_twitter.Api(consumer_key=CONSUMER_KEY, 
                                  consumer_secret=CONSUMER_SECRET,
                                  access_token_key=access_token.key,
                                  access_token_secret=access_token.secret)
        
         
        try:
            userinfo = twitter_api.VerifyCredentials()
        except:
            # If we cannot get the user information, user cannot be authenticated
            return None
        userid = userinfo.GetId()

        user, created = User.objects.get_or_create(id=userid,
                                                   username=userid,
                                                   first_name=userinfo.name)
        if created:
            # no password set since we validating through twitter oauth
            user.set_unusable_password()
            user.save()

        # Get the user profile
        userprofile = user.get_profile()
        userprofile.screen_name = userinfo.GetScreenName()
        userprofile.access_token = access_token.to_string()
        userprofile.url = userinfo.url
        userprofile.location = userinfo.location
        userprofile.description = userinfo.description
        userprofile.profile_image_url = userinfo.profile_image_url
        if not userprofile.whale:
            whale = Whale(species=WhaleSpecies.getDefaultSpecies())
            whale.save()
            userprofile.whale = whale
        if not userprofile.active_classifier:
            userprofile.active_classifier = DEFAULT_CLASSIFIER
            userprofile.classifier_version = DEFAULT_CLASSIFIER_VERSION
        userprofile.save()
        return user
        
    
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None

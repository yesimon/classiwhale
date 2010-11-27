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

import twitter

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')

class TwitterBackend:
    """TwitterBackend for authentication
    """
    def authenticate(self, access_token):
        '''authenticates the token by requesting user information from twitter
        '''
        twitter_api = twitter.Api(username=CONSUMER_KEY, password=CONSUMER_SECRET,
                                  access_token_key=access_token.key,
                                  access_token_secret=access_token.secret)
        
        print twitter_api
        try:
            userinfo = twitter_api.VerifyCredentials()
        except:
            # If we cannot get the user information, user cannot be authenticated
            return None
        userid = userinfo.GetId()

        user, created = User.objects.get_or_create(id=userid)
        if created:
            # no password set since we validating through twitter oauth
            user.set_unusable_password()

        user.username = userid
        user.first_name = userinfo.name
        user.save()

        # Get the user profile
        userprofile = user.get_profile()
        userprofile.screen_name = userinfo.GetScreenName()
        userprofile.access_token = access_token.to_string()
        userprofile.url = userinfo.url
        userprofile.location = userinfo.location
        userprofile.description = userinfo.description
        userprofile.profile_image_url = userinfo.profile_image_url
        userprofile.save()
        return user
        
    
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None

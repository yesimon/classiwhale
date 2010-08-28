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
"""

from django.conf import settings
from django.contrib.auth.models import User

import twitter

import os
import sys

# parse_qsl moved to urlparse module in v2.6
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl

import oauth2 as oauth

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

class TwitterBackend:
    """TwitterBackend for authentication
    """
    def authenticate(self, access_token):
        '''authenticates the token by requesting user information from twitter
        '''
        twitter = twitter.Api(username=CONSUMER_KEY, password=CONSUMER_SECRET)
        twitter.SetCredentials(username=CONSUMER_KEY, password=CONSUMER_SECRET, 
                                access_token_key=access_token.key,
                                access_token_secret=access_token.secret)
        try:
            userinfo = twitter.VerifyCredentials()
        except:
            # If we cannot get the user information, user cannot be authenticated
            return None

        userid = userinfo.GetId()

        user, created = User.objects.get_or_create(username=userid)
        if created:
            # create and set a random password so user cannot login using django built-in authentication
            temp_password = User.objects.make_random_password(length=12)
            user.set_password(temp_password)

        user.first_name = userinfo.name
        user.save()

        # Get the user profile
        userprofile = user.get_profile()
        userprofile.screen_name = user.GetScreenName()
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

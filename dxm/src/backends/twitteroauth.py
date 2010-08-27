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


import oauthtwitter


CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')



class TwitterBackend:
    """TwitterBackend for authentication
    """
    def authenticate(self, access_token):
        '''authenticates the token by requesting user information from twitter
        '''
        twitter = oauthtwitter.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, access_token)
        try:
            userinfo = twitter.GetUserInfo()
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
from django.http import HttpResponseBadRequest
from piston.handler import BaseHandler
from status.models import Status
from twitterauth.models import Rating, UserProfile



class StatusHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Status
    exclude = () # shows primary key
    exclude = ('in_reply_to_user', 'in_reply_to_status',)
    @classmethod
    def read(self, request, id=None):
        pass


class RatingHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Rating 
    @classmethod
    def read(self, request, username=None, emitter_format=None):
        if not username: return HttpResponseBadRequest()
        try:
            user = UserProfile.objects.get(screen_name=username)
        except: return HttpResponseBadRequest("User doesn't exist")
        ratings = Rating.objects.filter(user_profile=user).select_related(
                                         'status', 'user_profile')
        return ratings


class UserProfileHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = UserProfile
    exclude = ('access_token', '_state', 'user')

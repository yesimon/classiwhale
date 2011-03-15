# Handlers for the API

from piston.handler import BaseHandler
from django.http import HttpResponseBadRequest
from twitter.models import Status, TwitterUserProfile, Rating
import prediction.views
from twitter.utils import get_authorized_twython, full_create_status
from prediction.views import get_filtered_friends_timeline
from piston.utils import rc

class TimelineHandler(BaseHandler):
    def read(self, request):
        user = request.user
        if not user.is_authenticated() or 'twitter_tokens' not in request.session:
            return rc.FORBIDDEN
        twitter_tokens = request.session['twitter_tokens']
        tp = TwitterUserProfile.objects.get(id=twitter_tokens['user_id'])
        api = get_authorized_twython(twitter_tokens)
        statuses = Status.construct_from_dicts(api.getFriendsTimeline())
        Rating.appendTo(statuses, tp)
        return {
                    'statuses': statuses
                }

class FilteredTimelineHandler(BaseHandler):
    def read(self, request):
        user = request.user
        if not user.is_authenticated() or 'twitter_tokens' not in request.session:
            return rc.FORBIDDEN
        return get_filtered_friends_timeline(request)

class FriendsHandler(BaseHandler):
    def read(self, request):
        user = request.user
        if not user.is_authenticated() or 'twitter_tokens' not in request.session:
            return rc.FORBIDDEN
        twitter_tokens = request.session['twitter_tokens']
        tp = TwitterUserProfile.objects.get(id=twitter_tokens['user_id'])
        api = get_authorized_twython(twitter_tokens)
        friends = api.getFriendsStatus()
        return { 'friends' : friends }
    
class RateHandler(BaseHandler):
    def read(self, request):
        return None
        

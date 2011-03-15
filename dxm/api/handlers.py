# Handlers for the API

from piston.handler import BaseHandler
from django.http import HttpResponseBadRequest
from twitter.models import Status, TwitterUserProfile, Rating
import prediction.views
from twitter.utils import get_authorized_twython, full_create_status
from prediction.views import get_filtered_friends_timeline
from piston.utils import rc
from twitter.views import get_rate_results, get_user_timeline_object

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
        lex = request.GET
        if (not lex.has_key(u'rating')) or (not (lex.has_key(u'status') or lex.has_key(u'id'))):
            return HttpResponseBadRequest("rating and/or status parameters missing")
        u = request.user
        if not u.is_authenticated():
            return rc.FORBIDDEN
        results = get_rate_results(request, lex)
        return results
    
class FriendTimelineHandler(BaseHandler):
    def read(self, request):
        lex = request.GET
        if (not lex.has_key(u'id')):
            return HttpResponseBadRequest("id parameter missing")
        
        user = request.user
        if not user.is_authenticated() or 'twitter_tokens' not in request.session:
            return rc.FORBIDDEN
        
        identifier = lex[u'id']
        if(lex.has_key(u'page')):
            timeline = get_user_timeline_object(request, identifier, lex[u'page'])
        else:
            timeline = get_user_timeline_object(request, identifier)
            
        twitter_tokens = request.session['twitter_tokens']
        tp = TwitterUserProfile.objects.get(id=twitter_tokens['user_id'])
        statuses = Status.construct_from_dicts(timeline)
        Rating.appendTo(statuses, tp)
        return {
                    'statuses': statuses
                }
        
        
        

# dxm/api/urls.py

from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import TimelineHandler, FilteredTimelineHandler, FriendsHandler, RateHandler, FriendTimelineHandler

# define a resource exempt to CSRF protection since
# most API requests will not come from our domain
class CsrfExemptResource(Resource):
    def __init__(self, handler, authentication = None):
        super( CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )
        

filter_resource = CsrfExemptResource(FilteredTimelineHandler)
timeline_resource = CsrfExemptResource(TimelineHandler)
friends_resource = CsrfExemptResource(FriendsHandler)
rate_resource = CsrfExemptResource(RateHandler)
friend_timeline_resource = CsrfExemptResource(FriendTimelineHandler)
    
urlpatterns = patterns('',
                          (r'^twitter/timeline/$', timeline_resource),
                          (r'^twitter/filtered/$', filter_resource),
                          (r'^twitter/friends/', friends_resource),
                          (r'^twitter/friend/timeline/', friend_timeline_resource),
                          (r'^twitter/rate/', rate_resource),
                       )
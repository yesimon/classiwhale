from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import RatingHandler
from api.authentication import DjangoAuthentication


auth = DjangoAuthentication()
ad = {'authentication': auth}

rating_handler = Resource(RatingHandler, **ad)



urlpatterns = patterns('',
    url(r'^ratings/(?P<username>\w+).(?P<emitter_format>(json|xml|yaml|pickle|django))$', rating_handler),
        
)

from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from twitterauth.models import UserProfile, Rating


class RatingResource(ModelResource):
    # Custom filter for getting user ratings
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
            
        if "user" in filters:
            prof = UserProfile.objects.get(screen_name=filters['user'])
            orm_filters = {"user_profile__exact": prof}
        else:
            orm_filters = {}
        return orm_filters
    class Meta:
        # More modifications necessary for authentication and limiting later
        queryset = Rating.objects.all()
        list_allowed_methods = ['get']

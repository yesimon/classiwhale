from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from twitterauth.models import UserProfile, Rating
from twitterauth.api.auth import TwitterauthAuthorization
from status.api.resources import StatusResource

class UserProfileResource(ModelResource):
    ratings = fields.ToManyField('twitterauth.api.resources.RatingResource', 'ratings')

    class Meta:
        queryset = UserProfile.objects.all()
        list_allowed_methods = ['get']
        fields = ['id', 'profile_image_url', 'screen_name', 'location',
                    'description', 'ratings']

class RatingResource(ModelResource):
    status = fields.ForeignKey(StatusResource, 'status', full=True)
    user = fields.ForeignKey(UserProfileResource, 'user_profile')

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
        excludes = ['id']
        authentication = Authentication()
        authorization = TwitterauthAuthorization()
        include_resource_uri = False

from tastypie.resources import ModelResource
from twitterauth.api.auth import TwitterauthAuthorization
from status.models import Status

class StatusResource(ModelResource):

    class Meta:
        queryset = Status.objects.all()
        list_allowed_methods = ['get']
        authorization = TwitterauthAuthorization()
        fields = ['created_at', 'text', 'id']
        include_resource_uri = False

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

class TwitterauthAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            prof = request.user.get_profile()
            return object_list.filter(user_profile__exact=prof)
        return object_list.none()

from twitter.models import *

def twitter_user(request):
    try:
        user = request.user
    except AttributeError:
        return {}
    if not user.is_authenticated():
        return {}
    try:
        twitter_user = TwitterUserProfile.objects.get(id=request.session['twitter_tokens']['user_id'])
    except:
        return {}
    return {'twitter_user': twitter_user}

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from status.models import Status
from twitterauth.utils import get_authorized_twitter_api
import twitter
import json



@login_required
def user_search_index(request):    
    searchString = request.GET.get('q')
    if searchString is not None:
        api = authorize_twitter_api(request.session['access_token'])
        statuses = api.GetUserTimeline(id=searchString)
        template = 'user_search_results.html'
        data = {
            'user_statuses': statuses,
        }
        return render_to_response(template, data, 
                                   context_instance=RequestContext(request))


def ajax_user_search(request):
    if request.is_ajax():
        searchString = request.GET.get('q')
        if searchString is not None:
            api = authorize_twitter_api(request.session['access_token'])
            statuses = api.GetUserTimeline(id=searchString)
            template = 'user_search_results.html'
            data = {
                'user_statuses': statuses,
            }
            return render_to_response(template, data, 
                                       context_instance=RequestContext(request))
        

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from status.models import Status
from twitterauth.utils import get_authorized_twitter_api
import twitter
import json



@login_required
def index(request):    
    term = request.GET.get('q')
    if term is not None:
        api = get_authorized_twitter_api(request.session['access_token'])
        statuses = api.GetSearch(term=term)
        return  render_to_response('index.html', {
                    'statuses': statuses,
                    'term': term
                }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required
def ajax_index(request):
    if request.is_ajax():
        term = request.GET.get('q')
        page = request.GET.get('page')
        if (term is not None and page is not None):
            api = get_authorized_twitter_api(request.session['access_token'])
            statuses = api.GetSearch(term=term, page=page)
            return render_to_response('status_list.html', {
                                         'statuses': statuses
                                      }, context_instance=RequestContext(request))
    return HttpResponse('')





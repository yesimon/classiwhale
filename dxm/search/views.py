from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import json

from twython import Twython
from twitter.models import *
from twitter.utils import get_authorized_twython



def index(request):    
    if not request.user.is_authenticated() or 'twitter_tokens' not in request.session:
        return HttpResponseRedirect("/")
    
    term = request.GET.get('q')
    if term is not None:
        api = get_authorized_twython(request.session['twitter_tokens'])
        statuses = TwitterUserProfile.construct_from_dicts(api.searchUsers(q=term))
        return  render_to_response('search_index.html', {
                    'statuses': statuses,
                    'term': term
                }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def ajax_index(request):
    if not request.user.is_authenticated() or 'twitter_tokens' not in request.session:
        return HttpResponse("")
    if request.is_ajax():
        term = request.GET.get('q')
        page = request.GET.get('page')
        if (term is not None and page is not None):
            api = get_authorized_twython(request.session['twitter_tokens'])
            statuses = TwitterUserProfile.construct_from_dicts(api.searchUsers(q=term))
            return render_to_response('twitter/status_list.html', {
                                         'statuses': statuses
                                      }, context_instance=RequestContext(request))
    return HttpResponse('')





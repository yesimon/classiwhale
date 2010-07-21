from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.core.exceptions import ObjectDoesNotExist
from tweed.tweet.models import Status
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from tweed.accounts.models import UserProfile, StatusDetails
import twitter
import json
import time



def RecentPublicPosts(request):
    api = twitter.Api()
    recentStatuses = api.GetPublicTimeline()
    statusJson = recentStatuses[0].AsJsonString()
    jsonPackage = json.dumps([j.AsJsonString() for j in recentStatuses])
    return render_to_response('public_posts.html',
        {'recentStatuses': recentStatuses, 
        'statusJson': statusJson,
        'jsonPackage': jsonPackage},
        context_instance=RequestContext(request))


@login_required
def rate(request):
    results = {'success':'False'}
    if request.method != u'POST':
        return HttpResponseBadRequest("Only allows POST requests")
    POST = request.POST
    if (not POST.has_key(u'rating')) or (not POST.has_key(u'id')):
        return HttpResponseBadRequest("rating and/or id parameters missing")
    (u, id, rating) = (request.user, int(POST[u'id']), POST[u'rating'])
    prof = u.get_profile()
    try:
        s = Status.objects.get(id=id)
    except:
        s = Status.objects.create(id=id)
    try:
        details = StatusDetails.objects.get(user_profile=prof, status=s)
    except:
        details = StatusDetails.objects.create(status=s, user_profile=prof, rating=0)
    if rating == u"up":
        details.rating=1
    elif rating == u"down":
        details.rating=-1
    details.save()
    results['success'] = 'True'
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')
  


@login_required
def list_statuses(request):
    prof = request.user.get_profile()
    statusObjects = prof.statuses.iterator()
    statuses_like = []
    statuses_dislike = []
    api = twitter.Api()
    for statusObject in statusObjects:
        try:
            s = api.GetStatus(statusObject.id)
            details = StatusDetails.objects.get(status=statusObject, user_profile=prof)
            if details.rating > 0:
                statuses_like.append(s)
            elif details.rating < 0:
                statuses_dislike.append(s)
            else:
                pass
        except:
            pass
    return render_to_response('statuses_list_page.html',
        {'statuses_like': statuses_like,
        'statuses_dislike': statuses_dislike},
        context_instance=RequestContext(request)) 
        


@login_required
def user_search_index(request):    
    template = 'user_search_index.html'
    data = {
    }
    return render_to_response(template, data, 
                               context_instance=RequestContext(request))

def ajax_user_search(request):
    if request.is_ajax():
        searchString = request.GET.get('q')
        if searchString is not None:
            api = twitter.Api()
            statuses = api.GetUserTimeline(user=searchString)
            template = 'user_search_results.html'
            data = {
                'user_statuses': statuses,
            }
            return render_to_response(template, data, 
                                       context_instance=RequestContext(request))
        

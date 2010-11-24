from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from twitterauth.models import *
from twitterauth.utils import get_authorized_twitter_api
from status.models import *
from django.template.loader import get_template
import twitter
import json
import time


def recent_public_posts(request):
    api = twitter.Api()
    statuses = api.GetPublicTimeline()
#    statusJson = recentStatuses[0].AsJsonString()
#    jsonPackage = json.dumps([j.AsJsonString() for j in recentStatuses])
    statusJson, jsonPackage = None, None
    return render_to_response('public_posts.html',
        {'statuses': statuses, },
        context_instance=RequestContext(request))


def ajax_recent_public_posts(request):
    results = {'success': 'False'}
    api = twitter.Api()
#    since_id = request.GET.since_id
    results['statuses'] = api.GetPublicTimeline()
    t = get_template('status_list.html')
    results['success'] = 'True'
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)


def friends_timeline(request):
    if not request.user.is_authenticated() or 'access_token' not in request.session:
        return HttpResponseRedirect(reverse('status.views.recent_public_posts'))
    api = get_authorized_twitter_api(request.session['access_token'])
    statuses = api.GetFriendsTimeline()
    friends = api.GetFriends()
    return render_to_response('friends_timeline.html',
        {'statuses': statuses,
        'friends': friends,},
        context_instance=RequestContext(request))


def ajax_friend_timeline(request):
    results = {'success': 'False'}
    if request.method != u'GET':
        return HttpResponseBadRequest('Must be GET request')
    if not request.GET.has_key(u'screenname'):
        return HttpResponseBadRequest('friend screenname missing')
    screenname = request.GET[u'screenname']
    Api = twitter.Api()
    api = get_authorized_twitter_api(request.session['access_token'])
    results['statuses'] = api.GetUserTimeline(id=screenname)
    t = get_template('status_list.html')
    results['success'] = 'True'
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)




@login_required

def ajax_rate(request):
    results = {'success':'False'}
    if request.method != u'POST':
        return HttpResponseBadRequest("Only allows POST requests")
    POST = request.POST
    
    if (not POST.has_key(u'rating')) or (not POST.has_key(u'id')):
        return HttpResponseBadRequest("rating and/or id parameters missing")
    (u, id, rating) = (request.user, int(POST[u'id']), POST[u'rating'])
    prof = u.get_profile()
    
    s, c = Status.objects.get_or_create(id=id)
    r, c = Rating.objects.get_or_create(status=s, user_profile=prof)
    
    if rating == u"up":
        r.rating = 1
    elif rating == u"down":
        r.rating = -1
    r.save()
    results['success'] = 'True'
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')
  
  
  
def list_statuses(request):
    prof = request.user.get_profile()
    statusObjects = prof.statuses.iterator()
    statuses_like = []
    statuses_dislike = []
    api = get_authorized_twitter_api(request.session['access_token'])
    for statusObject in statusObjects:
        try:
            s = api.GetStatus(statusObject.id)
            details = Status.objects.get(status=statusObject, user_profile=prof)
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
        


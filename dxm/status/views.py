from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from twitterauth.models import UserProfile, StatusDetails
from twitterauth.utils import get_authorized_twitter_api
from status.models import Status
from django.template.loader import get_template
import twitter
import json
import time


def recent_public_posts(request):
    api = twitter.Api()
    recentStatuses = api.GetPublicTimeline()
#    statusJson = recentStatuses[0].AsJsonString()
#    jsonPackage = json.dumps([j.AsJsonString() for j in recentStatuses])
    statusJson, jsonPackage = None, None
    return render_to_response('public_posts.html',
        {'recentStatuses': recentStatuses, },
        context_instance=RequestContext(request))


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
    api = get_authorized_twitter_api(request.session['access_token'])
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
        


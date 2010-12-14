from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.paginator import Paginator
from twitterauth.models import *
from twitterauth.utils import get_authorized_twitter_api
from status.models import *
import twitter
import json
import time


def recent_public_posts(request):
    api = twitter.Api()
    statuses = api.GetPublicTimeline()
    return render_to_response('public_posts.html',
        {'statuses': statuses, },
        context_instance=RequestContext(request))


def ajax_recent_public_posts(request):
    '''Get more recent public posts via ajax - currently does not support 
    checking of the latest since_id for already down tweets'''
    results = {'success': 'False'}
    api = twitter.Api()
#    since_id = request.GET.since_id
    results['statuses'] = api.GetPublicTimeline()
    t = get_template('status_list.html')
    results['success'] = 'True'
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)



@login_required
def rating_history(request):
    """Returns list of dicts giving tweet id and rating (like/dislike) for rated tweets"""
    # Paginator generates two database queries unfortunately - negating benefits?
    prof = request.user.get_profile()
    ratings_list = Rating.objects.filter(user_profile=prof).order_by('-rated_time')
    ratings = []
    rating_paginator = Paginator(ratings_list, 10)
    r_page = rating_paginator.page(1).object_list
    for detail in r_page:
        if detail.rating > 0: rating = 'like'
        elif detail.rating < 0: rating = 'dislike'
        else: pass
        ratings.append({'id':detail.status_id, 'rating':rating})
    return render_to_response('rating_history.html',
        {'ratings': ratings},
        context_instance=RequestContext(request)) 
        
def training_login(request):
    return HttpResponseRedirect('/accounts/login/?next=/training/')
        
@login_required
def training_set_posts(request):
    """Returns list of unrated training tweets paginated"""
    prof = request.user.get_profile()
    statuses = prof.training_statuses.exclude(
        rating__user_profile__exact=prof.pk).order_by(
        '-created_at')[:20]
    author_ids = set([s.author_id for s in statuses])
    authors = UserProfile.objects.in_bulk(author_ids)
    for status in statuses:
        status.screen_name = authors[status.author_id].screen_name
        status.profile_image_url = authors[status.author_id].profile_image_url
    return render_to_response('training_set_posts.html',
        {'statuses': statuses},
        context_instance=RequestContext(request))

@login_required        
def ajax_training_set_posts(request):
    results = {'success': 'False'}
    if request.method != u'GET':
        return HttpResponseBadRequest('Must be GET request')
    if not request.GET.has_key(u'elements'):
        return HttpResponseBadRequest('Number of existing elements missing')
    num_shown_statuses = int(request.GET[u'elements'])
    prof = request.user.get_profile()
    statuses = prof.training_statuses.exclude(
        rating__user_profile__exact=prof.pk).order_by(
        '-created_at')[num_shown_statuses:num_shown_statuses+40] \
        .select_related()
    author_ids = set([s.author_id for s in statuses])
    authors = UserProfile.objects.in_bulk(author_ids)
    for status in statuses:
        status.screen_name = authors[status.author_id].screen_name
        status.profile_image_url = authors[status.author_id].profile_image_url
    t = get_template('training_set_list.html')
    results['success'] = 'True'
    results['statuses'] = statuses
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)


def public_profile(request, username):
    api = twitter.Api()
    statuses = api.GetUserTimeline(username)
    user = api.GetUser(username)
    return render_to_response('public_profile.html',
        {
         'user': user,
         'statuses': statuses
        },
        context_instance=RequestContext(request)) 
    
    

def ajax_friend_timeline(request):
    results = {'success': 'False'}
    if request.method != u'GET':
        return HttpResponseBadRequest('Must be GET request')
    if not request.GET.has_key(u'screenname'):
        return HttpResponseBadRequest('friend screenname missing')
    screenname = request.GET[u'screenname']
    api = get_authorized_twitter_api(request.session['access_token'])
    results['statuses'] = api.GetUserTimeline(id=screenname)
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
    
    Rating.appendTo(statuses, request.user.get_profile())
    
    return render_to_response('friends_timeline.html',
        {
         'statuses': statuses,
        'friends': friends
        },
        context_instance=RequestContext(request))


def ajax_rate(request):
    results = {'success':'False'}
    if request.method != u'POST':
        return HttpResponseBadRequest("Only allows POST requests")
    POST = request.POST    
    if (not POST.has_key(u'rating')) or (not POST.has_key(u'id')):
        return HttpResponseBadRequest("rating and/or id parameters missing")
    (u, id, rating) = (request.user, int(POST[u'id']), POST[u'rating'])
    if !u.is_authenticated:
        return HttpResponse(status=400)
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
  
  
  

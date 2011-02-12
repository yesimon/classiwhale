from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
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
from datetime import datetime
from email.utils import parsedate
from time import mktime
import twitter
import json


def public_timeline(request):
    api = twitter.Api()
    statuses = api.GetPublicTimeline()
    return render_to_response('public_timeline.html',
        {'statuses': statuses},
        context_instance=RequestContext(request))


def ajax_public_timeline(request):
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
    prof_ids = set([s.user_profile_id for s in statuses])
    profs = UserProfile.objects.in_bulk(prof_ids)
    for status in statuses:
        status.screen_name = profs[status.user_profile_id].screen_name
        status.profile_image_url = profs[status.user_profile_id].profile_image_url
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
    prof_ids = set([s.user_profile_id for s in statuses])
    authors = UserProfile.objects.in_bulk(prof_ids)
    for status in statuses:
        status.screen_name = authors[status.user_profile_id].screen_name
        status.profile_image_url = authors[status.user_profile_id].profile_image_url
    t = get_template('training_set_list.html')
    results['success'] = 'True'
    results['statuses'] = statuses
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)


def public_profile(request, username):
    api = twitter.Api()
    user = request.user
    if request.user.is_authenticated() and 'access_token' in request.session: #authenticate if possible
        api = get_authorized_twitter_api(request.session['access_token'])
    friend = api.GetUser(username)
    
    friends = api.GetFriends()
    prof = user.get_profile()
    
    try:
        statuses = api.GetUserTimeline(username)
        Rating.appendTo(statuses, prof)
    except twitter.TwitterError as err:
        outgoing = api.FriendshipsOutgoing()
        follow_request_sent = False
        if(user.id in outgoing):
            follow_request_sent = True
            
        return render_to_response('protected_profile.html',
            {
             'whale': prof.whale,
             'friends': friends,
             'username': username,
             'friend': friend,
             'follow_request_sent': follow_request_sent
             },
             context_instance=RequestContext(request)) 
    max_id = statuses[0].GetId()
    
    return render_to_response('public_profile.html',
        {
         'whale': prof.whale,
         'friends': friends,
         'username': username,
         'friend': friend,
         'statuses': statuses,
         'max_id': max_id
        },
        context_instance=RequestContext(request)) 
    

def ajax_user_timeline(request):
    results = {'success': 'False'}
    if request.method != u'GET':
        return HttpResponseBadRequest('Must be GET request')
    if not request.GET.has_key(u'screenname'):
        return HttpResponseBadRequest('screenname missing')
    if not request.GET.has_key(u'max_id'):
        return HttpResponseBadRequest('start id missing')
    if not request.GET.has_key(u'page'):
        return HttpResponseBadRequest('page number missing')
    screenname = request.GET[u'screenname']
    max_id = request.GET[u'max_id']
    page = request.GET[u'page']
    
    api = twitter.Api()
    if request.user.is_authenticated() and 'access_token' in request.session: #authenticate if possible
        api = get_authorized_twitter_api(request.session['access_token'])
    results['statuses'] = api.GetUserTimeline(id=screenname, max_id=max_id, page=page)
    t = get_template('status_list.html')
    results['success'] = 'True'
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)



def ajax_timeline(request):
    if not request.user.is_authenticated() or 'access_token' not in request.session:
        return HttpResponseRedirect(reverse('status.views.public_timeline'))
    api = get_authorized_twitter_api(request.session['access_token'])
    
    if not request.GET.has_key(u'page'):
        return HttpResponseBadRequest('page number missing')
    page = request.GET[u'page']
    
    statuses = api.GetFriendsTimeline(page=page)
    # this next call is slow as hell, not efficient
    Rating.appendTo(statuses, request.user.get_profile())
    return render_to_response('status_list.html',
        {
          'statuses': statuses
        },
        context_instance=RequestContext(request))
    
def timeline(request):
    user = request.user
    if not user.is_authenticated() or 'access_token' not in request.session:
        return HttpResponseRedirect(reverse('status.views.public_timeline'))
#    if 'access_token' not in request.session:
#        return HttpResponseRedirect(reverse('status.views.public_timeline'))
#    prof = UserProfile.objects.get(pk=request.session['_auth_user_id'])
    api = get_authorized_twitter_api(request.session['access_token'])
    
    statuses = api.GetFriendsTimeline()
    friends = api.GetFriends()
    prof = user.get_profile()
    Rating.appendTo(statuses, prof)
    
    return render_to_response('timeline.html',
        {
          'whale': prof.whale,
          'statuses': statuses,
          'friends': friends
        },
        context_instance=RequestContext(request))

def full_create_status(status):
    try: u = User.objects.get(id=status.user.id)
    except User.DoesNotExist:
        u = User(id=status.user.id, username=status.user.id)
        u.save()
    try: prof = UserProfile.objects.get(pk=status.user.id)
    except UserProfile.DoesNotExist:
        prof = UserProfile(pk=status.user.id)
        prof.save()
    status = Status(
        id=status.id,
        text=status.text,
        user_profile=prof,
        created_at=datetime.fromtimestamp(mktime(parsedate(status.created_at))),
        content_length=len(status.text),
        )
    status.save()
    return status


def ajax_rate(request):
    results = {'success':'False'}
    if request.method != u'POST':
        return HttpResponseBadRequest("Only allows POST requests")
    POST = request.POST
    if (not POST.has_key(u'rating')) or (not POST.has_key(u'status')):
        return HttpResponseBadRequest("rating and/or status parameters missing")
    u, rating, status = (request.user, POST[u'rating'], 
                         twitter.Status.NewFromJsonDict(json.loads(POST[u'status'])))
    if not u.is_authenticated():
        return HttpResponseBadRequest("Must be logged in")
    prof = u.get_profile()
    s = full_create_status(status)
    """p
    s, c = Status.objects.get_or_create(id=status.id, text=status.text,     \
                created_at=datetime.fromtimestamp(mktime(     \
                parsedate(status.created_at))))
    """
    if rating == u"up":
        rating_int = 1
    elif rating == u"down":
        rating_int = -1
    r = Rating(status=s, user_profile=prof, rating=rating_int)
    r.save()
    prof.whale.exp = prof.whale.exp + 1
    if prof.whale.exp == prof.whale.species.evolution.minExp:
        prof.whale.species = prof.whale.species.evolution
    prof.whale.save()
    results['success'] = 'True'
    results['exp'] = prof.whale.exp
    results['min-exp'] = prof.whale.species.minExp
    results['max-exp'] = prof.whale.species.evolution.minExp
    results['species'] = prof.whale.species.img.url
    results['speciesName'] = prof.whale.species.name
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')
  
  
def post_status(request):
    results = {'success':'False'}
    user = request.user
    if not user.is_authenticated() or 'access_token' not in request.session:
        return HttpResponseRedirect(reverse('status.views.public_timeline'))
    API = get_authorized_twitter_api(request.session['access_token'])
    status = request.POST[u'status']
    print("about to post status")
    try:
        API.PostUpdate(status)
        results['success'] = 'True'
    except twitter.TwitterError:
        pass
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')


def create_friendship(request):
    results = {'success':'False'}
    user = request.user
    if not user.is_authenticated() or 'access_token' not in request.session:
        return HttpResponseRedirect(reverse('status.views.public_timeline'))
    API = get_authorized_twitter_api(request.session['access_token'])
    username = request.POST[u'friend_username']
    user_to_follow = API.GetUser(username)
    try:
        API.CreateFriendship(username)
        results['success'] = 'True'
    except twitter.TwitterError:
        pass
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')

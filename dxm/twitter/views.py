from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from email.utils import parsedate
from time import mktime
from twython import Twython, TwythonError
import json

from profile.models import UserProfile
from twitter.models import TwitterUserProfile, Status, Rating
from twitter.utils import get_authorized_twython, full_create_status

from whale.models import Whale, WhaleSpecies

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')

DEFAULT_CLASSIFIER = 'CylonBayesClassifier'
DEFAULT_CLASSIFIER_VERSION = '0.1'

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL')

    
"""
@login_required
def public_timeline(request):
    api = Twython()
    statuses = map(Status.construct_from_dict, api.getPublicTimeline())
    return render_to_response('twitter/public_timeline.html',
        {'statuses': statuses},
        context_instance=RequestContext(request))


def ajax_public_timeline(request):
    '''Get more recent public posts via ajax - currently does not support 
    checking of the latest since_id for already down tweets'''
    results = {'success': 'False'}
    api = Twython()
#    since_id = request.GET.since_id
    results['statuses'] = map(Status.construct_from_dict, api.getPublicTimeline())
    t = get_template('twitter/status_list.html')
    results['success'] = 'True'
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)
"""

def timeline(request):
    user = request.user
    if not user.is_authenticated() or 'twitter_tokens' not in request.session:
        return render_to_response('landing.html')
    twitter_tokens = request.session['twitter_tokens']
    user_profile = UserProfile.objects.get(user=user)
    tp = TwitterUserProfile.objects.get(id=twitter_tokens['user_id'])
    api = get_authorized_twython(twitter_tokens)
    statuses = Status.construct_from_dicts(api.getFriendsTimeline())
    friends = api.getFriendsStatus()
    Rating.appendTo(statuses, tp)
    return render_to_response('twitter/timeline.html',
        {
          'whale': user_profile.whale,
          'statuses': statuses,
          'friends': friends
        },
        context_instance=RequestContext(request))


def ajax_timeline(request):
    if not request.user.is_authenticated() or 'twitter_tokens' not in request.session:
        return HttpResponse("")
    twitter_tokens = request.session['twitter_tokens']
    api = get_authorized_twython(twitter_tokens)
    tp = TwitterUserProfile.objects.get(id=twitter_tokens['user_id'])
    if not request.GET.has_key(u'page'):
        return HttpResponseBadRequest('page number missing')
    page = request.GET[u'page']
    
    statuses = Status.construct_from_dicts(api.getFriendsTimeline(page=page))
    Rating.appendTo(statuses, tp)
    return render_to_response('twitter/status_list.html',
        {
          'statuses': statuses
        },
        context_instance=RequestContext(request))


def public_profile(request, username):
    if request.user.is_authenticated() and 'twitter_tokens' in request.session:
        twitter_tokens = request.session['twitter_tokens']
        api = get_authorized_twython(twitter_tokens)
    else: #require login
        return HttpResponseRedirect("/")
        # Get public api if no authentication possible
        #api = Twython()
    friend = api.showUser(screen_name=username)
    
    friends = api.getFriendsStatus()
    prof = request.user.get_profile()
    
    try:
        statuses = Status.construct_from_dicts(api.getUserTimeline(screen_name=username))
    except TwythonError:
        outgoing = api.friendshipsOutgoing()
        follow_request_sent = False
        if request.user.id in outgoing:
            follow_request_sent = True
        return render_to_response('twitter/protected_profile.html',
            {
             'whale': prof.whale,
             'friends': friends,
             'username': username,
             'friend': friend,
             'follow_request_sent': follow_request_sent
             },
             context_instance=RequestContext(request)) 
    return render_to_response('twitter/public_profile.html',
        {
         'whale': prof.whale,
         'friends': friends,
         'username': username,
         'friend': friend,
         'statuses': statuses,
        },
        context_instance=RequestContext(request)) 


def ajax_user_timeline(request):
    if not request.user.is_authenticated() or 'twitter_tokens' not in request.session:
        return HttpResponse("")
         
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
    
    if 'twitter_tokens' in request.session:
        twitter_tokens = request.session['twitter_tokens']
        api = get_authorized_twython(twitter_tokens)
    else: # Get public api if no authentication possible
        api = Twython()

    results['statuses'] = api.getUserTimeline(screen_name=screenname, max_id=max_id, page=page)
    t = get_template('twitter/status_list.html')
    results['success'] = 'True'
    html = t.render(RequestContext(request, results))
    return HttpResponse(html)


def post_status(request):
    results = {'success':'False'}
    if not request.user.is_authenticated() or 'twitter_tokens' not in request.session:
        return HttpResponse("")
    twitter_tokens = request.session['twitter_tokens']
    API = get_authorized_twython(twitter_tokens)
    status = request.POST[u'status']
    try:
        API.updateStatus(status=status)
        results['success'] = 'True'
    except TwythonError:
        pass
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')


def create_friendship(request):
    results = {'success':'False'}
    if not request.user.is_authenticated() or 'twitter_tokens' not in request.session:
        return HttpResponse("")
    twitter_tokens = request.session['twitter_tokens']
    API = get_authorized_twython(twitter_tokens)
    username = request.POST[u'friend_username']
    try:
        API.createFriendship(screen_name=username)
        results['success'] = 'True'
    except TwythonError:
        pass
    jsonResults = json.dumps(results)
    return HttpResponse(jsonResults, mimetype='application/json')


def ajax_rate(request):
    results = {'success':'False'}
    if request.method != u'POST':
        return HttpResponseBadRequest("Only allows POST requests")
    POST = request.POST
    if (not POST.has_key(u'rating')) or (not POST.has_key(u'status')):
        return HttpResponseBadRequest("rating and/or status parameters missing")
    u = request.user
    if not u.is_authenticated():
        return HttpResponseBadRequest("Must be logged in")

    rating = POST[u'rating']
    status = Status.construct_from_dict(json.loads(POST[u'status']))
    tp = TwitterUserProfile.objects.get(id=request.session['twitter_tokens']['user_id'])
    prof = u.get_profile()
    status.save_with_user()

    if rating == u"up":
        rating_int = 1
    elif rating == u"down":
        rating_int = -1
    try: r = Rating.objects.get(status=status, user=tp)
    except Rating.DoesNotExist: r = Rating(status=status, user=tp)
    r.rating = rating_int
    r.save()
    prof.whale.exp += 1
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


"""
def rating_history(request):
    #Returns list of dicts giving tweet id and rating (like/dislike) for rated tweets
    # Paginator generates two database queries unfortunately - negating benefits?
    twitter_tokens = request.session['twitter_tokens']
    tp = TwitterUserProfile.objects.get(id=twitter_tokens['user_id'])

    ratings_list = Rating.objects.filter(user=tp).order_by('-rated_time')
    ratings = []
    rating_paginator = Paginator(ratings_list, 10)
    r_page = rating_paginator.page(1).object_list
    for detail in r_page:
        if detail.rating > 0: rating = 'like'
        elif detail.rating < 0: rating = 'dislike'
        else: pass
        ratings.append({'id':detail.status_id, 'rating':rating})
    return render_to_response('twitter/rating_history.html',
        {'ratings': ratings},
        context_instance=RequestContext(request)) 
"""


def twitter_logout(request, next_page):
    logout(request)
    return HttpResponseRedirect(next_page)

def twitter_login(request, window_type='window'):
    """
    The view function that initiates the entire handshake.
    """
    # Instantiate Twython with the first leg of our trip.
    callback_url = 'http://%s%s' % (request.get_host(), reverse('twitter.views.twitter_return', args=[window_type]))
    api = Twython(
        twitter_token = CONSUMER_KEY,
        twitter_secret = CONSUMER_SECRET,
        callback_url = callback_url
	)
    
    # Request an authorization url to send the user to...
    auth_props = api.get_authentication_tokens()
    
    # Then send them over there, durh.
    request.session['request_token'] = auth_props
    return HttpResponseRedirect(auth_props['auth_url'])

def twitter_return(request, window_type):
    """
    A user gets redirected here after hitting Twitter and authorizing your
    app to use their data. 
    
    This is the view that stores the tokens you want
    for querying data. Pay attention to this.
    """
    # Now that we've got the magic tokens back from Twitter, we need to exchange
    # for permanent ones and store them...

    api = Twython(
        twitter_token = CONSUMER_KEY,
        twitter_secret = CONSUMER_SECRET,
        oauth_token = request.session['request_token']['oauth_token'],
        oauth_token_secret = request.session['request_token']['oauth_token_secret']
    )

    # Retrieve the tokens we want...
    twitter_tokens = api.get_authorized_tokens()

    api = get_authorized_twython(twitter_tokens)

    username = '@'.join([str(twitter_tokens['user_id']), 'twitter'])

    request.session['twitter_tokens'] = twitter_tokens

    # No need to call authorize because of get_authorized_tokens()

    # Probable bug - need to fix when TwitterUserProfile already exists without
    # user having logged in.
    try:
        user = User.objects.get(username=username)
        tp = TwitterUserProfile.objects.get(id=user.id)
    except:
        # Create User, UserProfile, TwitterUserProfile
        twitter_user = api.verifyCredentials()
        if 'error' in twitter_user:
            del request.session['access_token']
            del request.session['request_token']
            return HttpResponse("Unable to authenticate you!")            
        name = twitter_user['name'].split()
        first_name, last_name = name[0], name[1]

        user = User(username=username, first_name=first_name, last_name=last_name)
        user.set_unusable_password()
        user.save()

        up = UserProfile(user=user)
        whale = Whale(species=WhaleSpecies.getDefaultSpecies())
        whale.save()
        up.whale = whale
        up.save()

        tp = TwitterUserProfile()
        tp.__dict__.update(twitter_user)
        tp.user = up
        tp.oauth_token = twitter_tokens['oauth_token']
        tp.oauth_secret = twitter_tokens['oauth_token_secret']
        tp.active_classifier = DEFAULT_CLASSIFIER
        tp.classifier_version = DEFAULT_CLASSIFIER_VERSION
        tp.save()

    # Hack so don't have to call authenticate
    user.backend = 'twitter.auth.TwitterAuthentication'

    login(request, user)
    
    if window_type == 'popup':
        return render_to_response("twitter/twitter_return.html", {},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")




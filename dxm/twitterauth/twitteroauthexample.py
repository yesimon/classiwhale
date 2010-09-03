import oauth, httplib, simplejson, time, datetime

from django.http import *
from django.conf import settings
from django.shortcuts import render_to_response

SERVER = getattr(settings, 'OAUTH_SERVER', 'twitter.com')
REQUEST_TOKEN_URL = getattr(settings, 'OAUTH_REQUEST_TOKEN_URL', 'https://%s/twitter_app/request_token' % SERVER)
ACCESS_TOKEN_URL = getattr(settings, 'OAUTH_ACCESS_TOKEN_URL', 'https://%s/twitter_app/access_token' % SERVER)
AUTHORIZATION_URL = getattr(settings, 'OAUTH_AUTHORIZATION_URL', 'http://%s/twitter_app/authorize' % SERVER)

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_CONSUMER_SECRET')

# We use this URL to check if Twitters oAuth worked
TWITTER_CHECK_AUTH = 'https://twitter.com/account/verify_credentials.json'
TWITTER_FRIENDS = 'https://twitter.com/statuses/friends.json'

connection = httplib.HTTPSConnection(SERVER)
consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

# Shortcut around oauth.OauthRequest
def request(url, access_token, parameters=None):
    """
    usage: request( '/url/', your_access_token, parameters=dict() )
    Returns a OAuthRequest object
    """
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=access_token, http_url=url, parameters=parameters,
    )
    oauth_request.sign_request(signature_method, consumer, access_token)
    return oauth_request


def fetch_response(oauth_request, connection):
    url = oauth_request.to_url()
    connection.request(oauth_request.http_method,url)
    response = connection.getresponse()
    s = response.read()
    return s

def get_unauthorised_request_token():
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, http_url=REQUEST_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, consumer, None)
    resp = fetch_response(oauth_request, connection)
    token = oauth.OAuthToken.from_string(resp)
    return token


def get_authorisation_url(token):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=token, http_url=AUTHORIZATION_URL
    )
    oauth_request.sign_request(signature_method, consumer, token)
    return oauth_request.to_url()

def exchange_request_token_for_access_token(request_token):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=request_token, http_url=ACCESS_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, consumer, request_token)
    resp = fetch_response(oauth_request, connection)
    return oauth.OAuthToken.from_string(resp) 

def is_authenticated(access_token):
    oauth_request = request(TWITTER_CHECK_AUTH, access_token)
    json = fetch_response(oauth_request, connection)
    if 'screen_name' in json:
        return json
    return False

def get_friends(access_token):
    """Get friends on Twitter"""
    oauth_request = request(TWITTER_FRIENDS, access_token, {'page': page})
    json = fetch_response(oauth_request, connection)
    return json
    


### DJANGO VIEWS BELOW THIS LINE


def main(request):
    if request.get_host().startswith('www.') or '/labs/followers/' in request.path: # Should really be middleware
        return HttpResponseRedirect("http://fourmargins.com/labs/following/")
    if request.session.has_key('access_token'):
        return HttpResponseRedirect('/list/')
    else:
        return render_to_response('oauth/base.html')

def unauth(request):
    response = HttpResponseRedirect('/')
    request.session.clear()
    return response

def auth(request):
    "/auth/"
    token = get_unauthorised_request_token()
    auth_url = get_authorisation_url(token)
    response = HttpResponseRedirect(auth_url)
    request.session['unauthed_token'] = token.to_string()   
    return response

def return_(request):
    "/return/"
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie")
    token = oauth.OAuthToken.from_string(unauthed_token)   
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    access_token = exchange_request_token_for_access_token(token)
    response = HttpResponseRedirect('/list/')
    request.session['access_token'] = access_token.to_string()
    return response

def get_friends(request):
    users = []
    
    access_token = request.session.get('access_token', None)
    if not access_token:
        return HttpResponse("You need an access token!")
    token = oauth.OAuthToken.from_string(access_token)   
    
    # Check if the token works on Twitter
    auth = is_authenticated(token)
    if auth:
        # Load the credidentials from Twitter into JSON
        creds = simplejson.loads(auth)
        name = creds.get('name', creds['screen_name']) # Get the name
        
        # Get number of friends. The API only returns 100 results per page,
        # so we might need to divide the queries up.
        friends_count = str(creds.get('friends_count', '100'))
        pages = int( (int(friends_count)/100) ) + 1
        pages = min(pages, 10) # We only want to make ten queries
        
        
        
        for page in range(pages):
            friends = get_friends(token, page+1)
            
            # if the result is '[]', we've reached the end of the users friends
            if friends == '[]': break
            
            # Load into JSON
            json = simplejson.loads(friends)

            users.append(json)
    
    return render_to_response('oauth/list.html', {'users': users})
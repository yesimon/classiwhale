from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate

from urlparse import parse_qsl
import oauth2 as oauth


signature_method = oauth.SignatureMethod_HMAC_SHA1()

ROOT_URL = getattr(settings, 'ROOT_URL')
CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET')
OAUTH_CALLBACK_URL = ROOT_URL + 'twitterauth/return/'

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL')

CONSUMER = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

def twitter_login(request):
    if CONSUMER_KEY is None or CONSUMER_SECRET is None:
        # Django config must have a consumer key and secret
        raise Exception
    request_token = _get_request_token()

    request.session['request_token'] = request_token.to_string()
    return HttpResponseRedirect(_get_authorization_url(request_token))


def _get_request_token():
    oauth_client = oauth.Client(CONSUMER)
    oauth_client.set_signature_method(signature_method)
    #Requesting request token from Twitter
    resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'POST', force_auth_header=True, 
                                         parameters={'oauth_callback': OAUTH_CALLBACK_URL})
    if resp['status'] != '200':
        return HttpResponse("Invalid respond from Twitter requesting temp token: %s' % resp['status']")
    else:
        request_token_dict = dict(parse_qsl(content))
    request_token = oauth.Token(request_token_dict['oauth_token'], 
                                request_token_dict['oauth_token_secret'])
    return request_token

def _get_authorization_url(request_token):
    authorization_url = '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token.key)
    return authorization_url


def twitter_return(request):
    request_token_string = request.session.get('request_token', None)

    # If there is no request_token for session,
    #    means we didn't redirect user to twitter
    if not request_token_string:
        # Redirect the user to the login page,
        # So the user can click on the sign-in with twitter button
        return HttpResponse("We didn't redirect you to twitter...")

    request_token = oauth.Token.from_string(request_token_string)

    # If the token from session and token from twitter does not match
    #   means something bad happened to tokens
    if request_token.key != request.GET.get('oauth_token', 'no-token'):
        del request.session['request_token']
        # Redirect the user to the login page
        return HttpResponse("Something wrong! Tokens do not match...")

    # Comment out verifier if broken - doesn't seemed to be used by other implemenations
    request_token.set_verifier(request.GET.get('oauth_verifier'))

    # Generating and signing request for an access token
    access_token = _get_access_token(request_token)


    request.session['access_token'] = access_token.to_string()
    auth_user = authenticate(access_token=access_token)

    # if user is authenticated then login user
    if auth_user:
        login(request, auth_user)
    else:
        # We were not able to authenticate user
        # Redirect to login page
        del request.session['access_token']
        del request.session['request_token']
        return HttpResponse("Unable to authenticate you!")

    # authentication was successful, use is now logged in
    return HttpResponseRedirect(LOGIN_REDIRECT_URL)


def _get_access_token(request_token):
    oauth_client = oauth.Client(CONSUMER, token=request_token)
    oauth_client.set_signature_method(signature_method)
    resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', force_auth_header=True)
    access_token_dict = dict(parse_qsl(content))
    access_token = oauth.Token(access_token_dict['oauth_token'], access_token_dict['oauth_token_secret'])
    return access_token


##### My views


def twitter_logout(request, next_page):
    logout(request)
    return HttpResponseRedirect(next_page)
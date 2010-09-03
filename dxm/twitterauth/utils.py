from django.conf import settings

import twitter
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

def get_authorized_twitter_api(access_token_string):
    access_token = oauth.Token.from_string(access_token_string)
    api = twitter.Api(username=CONSUMER_KEY,
                      password=CONSUMER_SECRET,
                      access_token_key=access_token.key,
                      access_token_secret=access_token.secret
                      )
    return api


def get_request_token():
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

def get_authorization_url(request_token):
    authorization_url = '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token.key)
    return authorization_url

def get_access_token(request_token):
    oauth_client = oauth.Client(CONSUMER, token=request_token)
    oauth_client.set_signature_method(signature_method)
    resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', force_auth_header=True)
    access_token_dict = dict(parse_qsl(content))
    access_token = oauth.Token(access_token_dict['oauth_token'], access_token_dict['oauth_token_secret'])
    return access_token

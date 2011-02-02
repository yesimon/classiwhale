import nexus
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from tastypie.api import Api
from twitterauth.api.resources import RatingResource, UserProfileResource
from status.api.resources import StatusResource
import mimetypes

URL_LIST = {
    'About'     : 'about/',
    'Home'      : 'twitter/',
    'Recent'    : 'twitter/recent/',
    'Search'    : 'twitter/search/',
}

admin.autodiscover()
nexus.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(RatingResource())
v1_api.register(UserProfileResource())
v1_api.register(StatusResource())

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'status.views.timeline'),
    (r'^admin/', include(admin.site.urls)),
    (r'^nexus/', include(nexus.site.urls)),
#    (r'^doc/(?P<template>.*)$', login_required(direct_to_template), {'mimetype':mimetypes.guess_type(template)}),
    (r'^api/', include(v1_api.urls)),
    (r'^sentry/', include('sentry.urls')),
    (r'^corsair/', include('corsair.urls')),
    (r'^about/$', direct_to_template, {'template': 'about.html' }),
    (r'^about/(\w+)/$', 'about_pages'),
    (r'^twitterauth/login/$', 'twitterauth.views.twitter_login'),
    (r'^twitterauth/login/(?P<window_type>\w+)/$', 'twitterauth.views.twitter_login'),
    (r'^twitterauth/return/(\w+)/$', 'twitterauth.views.twitter_return'),
    (r'^twitterauth/logout/$', 'twitterauth.views.twitter_logout', {'next_page': '/'}),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':
        'login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', 
        {'login_url': '/accounts/login/'}),
        
    (r'^status/recent/$', 'status.views.public_timeline'),
    (r'^status/ajax_rate/$', 'status.views.ajax_rate'),
    (r'^status/ajax_public_timeline/$', 'status.views.ajax_public_timeline'),
    (r'^status/ajax_user_timeline/$', 'status.views.ajax_user_timeline'),
    (r'^status/ajax_timeline/$', 'status.views.ajax_timeline'),
    (r'^status/ajax_training_set_posts/$', 'status.views.ajax_training_set_posts'),
    (r'^status/post/$', 'status.views.post_status'),
    (r'^status/create_friendship/$', 'status.views.create_friendship'),
    (r'^history/$', 'status.views.rating_history'),
    (r'^profile/(?P<username>\w+)/$', 'status.views.public_profile'),
    (r'^login/$', 'status.views.training_login'),
    (r'^training/$', 'status.views.training_set_posts'),
    
    (r'^search/$', 'search.views.index'),
    (r'^search/ajax/$', 'search.views.ajax_index'),
    
    (r'^feedback/ajax/(.*?)$', 'feedback.views.handle_ajax'),
    
    (r'^bayes/train/$', 'prediction.views.train_multinomial_bayes'),
    (r'^bayes/predict/$', 'prediction.views.predicted_friends_timeline'),
    (r'^bayes/filter/$', 'prediction.views.filtered_friends_timeline'),
    (r'^algorithm/train/$', 'prediction.views.train_classifier'),
    (r'^algorithm/predict/$', 'prediction.views.predicted_friends_timeline')
)

urlpatterns += patterns('contact.views',
    (r'^contact/$', 'contact'),
)

if settings.STATIC_SERVE:    
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )                           

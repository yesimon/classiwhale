from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
from tastypie.api import Api
from twitterauth.api.resources import RatingResource


URL_LIST = {
    'About'     : 'about/',
    'Home'      : 'twitter/',
    'Recent'    : 'twitter/recent/',
    'Search'    : 'twitter/search/',
}

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(RatingResource())


urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'status.views.timeline'),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
    (r'^sentry/', include('sentry.urls')),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html' }),
    (r'^about/(\w+)/$', 'about_pages'),
    (r'^twitterauth/login/$', 'twitterauth.views.twitter_login'),
    (r'^twitterauth/return/$', 'twitterauth.views.twitter_return'),
    (r'^twitterauth/logout/$', 'twitterauth.views.twitter_logout', {'next_page': '/'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':
        'login.html'}),
    (r'^login/$', 'status.views.training_login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', 
        {'login_url': '/accounts/login/'}),
    (r'^status/recent/$', 'status.views.public_timeline'),
    (r'^status/ajax_rate/$', 'status.views.ajax_rate'),
    (r'^status/ajax_public_timeline/$', 'status.views.ajax_public_timeline'),
    (r'^status/ajax_user_timeline/$', 'status.views.ajax_user_timeline'),
    (r'^status/ajax_timeline/$', 'status.views.ajax_timeline'),
    (r'^history/$', 'status.views.rating_history'),
    (r'^training/$', 'status.views.training_set_posts'),
    (r'^status/ajax_training_set_posts/$', 'status.views.ajax_training_set_posts'),
    (r'^search/$', 'search.views.user_search_index'),
    (r'^profile/(?P<username>\w+)/$', 'status.views.public_profile'),
    (r'^search/user/$', 'search.views.ajax_user_search'),
    (r'^feedback/ajax/(.*?)$', 'feedback.views.handle_ajax'),
#    (r'^bayes/train/$', 'classifier.views.train_multinomial_bayes'),
#    (r'^bayes/predict/$', 'classifier.views.predicted_friends_timeline'),
)

urlpatterns += patterns('contact.views',
    (r'^contact/$', 'contact'),
)

if settings.STATIC_SERVE:    
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )                           

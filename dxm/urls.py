from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from django.conf import settings

URL_LIST = {
    'About'     : 'about/',
    'Home'      : 'twitter/',
    'Recent'    : 'twitter/recent/',
    'Search'    : 'twitter/search/',
}

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'status.views.friends_timeline'),
    (r'^admin/', include(admin.site.urls)),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html' }),
    (r'^about/(\w+)/$', 'about_pages'),
    (r'^twitterauth/login/$', 'twitterauth.views.twitter_login'),
    (r'^twitterauth/return/$', 'twitterauth.views.twitter_return'),
    (r'^twitterauth/logout/$', 'twitterauth.views.twitter_logout', {'next_page': '/'}),
    (r'^status/recent/$', 'status.views.recent_public_posts'),
    (r'^status/ajax_rate/$', 'status.views.ajax_rate'),
    (r'^status/ajax_public_posts/$', 'status.views.ajax_recent_public_posts'),
    (r'^status/ajax_friend_timeline/$', 'status.views.ajax_friend_timeline'),
    (r'^history/$', 'status.views.rating_history'),
    (r'^search/$', 'search.views.user_search_index'),
    (r'^profile/(?P<username>\w+)/$', 'status.views.public_profile'),
    (r'^search/user/$', 'search.views.ajax_user_search'),
    (r'^feedback/ajax/(.*?)$', 'feedback.views.handle_ajax'),
)

urlpatterns += patterns('contact.views',
    (r'^contact/$', 'contact'),
)

if settings.DEBUG:    
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )                           

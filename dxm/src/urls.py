from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail


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

    (r'^$', 'tweet.views.list_statuses'),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './static/'}),
    (r'^about/$', direct_to_template, {'template': 'about.html' }),
    (r'^about/(\w+)/$', 'about_pages'),
    (r'^login/$', 'twitterauth.views.twitter_signin'),
    (r'^return/$', 'twitterauth.views.twitter_return'),
    #(r'^twitter/recent/$', 'tweet.views.RecentPublicPosts'),
    #(r'^twitter/rate/$', 'tweet.views.rate'),
    #(r'^twitter/$', 'tweet.views.list_statuses'),
    #(r'^twitter/search/$', 'tweet.views.user_search_index'),
    #(r'^twitter/search/user/$', 'tweet.views.ajax_user_search'),
    #(r'^twitter_app/', include('twitter_app.urls')),
)

urlpatterns += patterns('contact.views',
    (r'^contact/$', 'contact'),
)

    

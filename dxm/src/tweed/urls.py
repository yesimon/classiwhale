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

    (r'^$', 'tweed.tweet.views.list_statuses'),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './static/'}),
    (r'^about/$', direct_to_template, {'template': 'about.html' }),
    (r'^about/(\w+)/$', 'about_pages'),
    (r'^accounts/login/$',  login, {'template_name': 'login.html'}),
    (r'^accounts/logout/$', logout, {'template_name': 'logged_out.html'}),
    (r'^accounts/register/$', 'tweed.accounts.views.register'),
    (r'^twitter/recent/$', 'tweed.tweet.views.RecentPublicPosts'),
    (r'^twitter/rate/$', 'tweed.tweet.views.rate'),
    (r'^twitter/$', 'tweed.tweet.views.list_statuses'),
    (r'^twitter/search/$', 'tweed.tweet.views.user_search_index'),
    (r'^twitter/search/user/$', 'tweed.tweet.views.ajax_user_search'),
)

urlpatterns += patterns('tweed.contact.views',
    (r'^contact/$', 'contact'),
)

    
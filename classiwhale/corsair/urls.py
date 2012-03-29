import os
import re
from django.conf.urls.defaults import *

from corsair import views

CORSAIR_ROOT = os.path.dirname(__file__)

urlpatterns = patterns('',
    url(r'^_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(CORSAIR_ROOT, 'media')}, name='corsair-media'),

    url(r'^login/$', views.login, name='corsair-login'),
    url(r'^logout/$', views.logout, name='corsair-logout'),
    url(r'^$', views.index, name='corsair'),
    url(r'^training_sets/$', views.training_sets, name='corsair-training_sets'),
    url(r'^benchmarks/$', views.benchmarks, name='corsair-benchmarks'),
    url(r'^benchmarks/(.*?)/$', views.benchmark_detail, name='corsair-benchmark_detail'),
    url(r'^ajax/api/(?P<action>.*?)/$', views.ajax_api, name='corsair-ajax_api'),
)
               

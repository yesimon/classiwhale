# dxm/v1/urls.py

from django.conf.urls.defaults import *
import settings
import os
    
urlpatterns = patterns('',
                          (r'^$', 'v1.views.index'),
                       )

if settings.STATIC_SERVE: 
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.ROOT_PROJECT_PATH, 'v1/static/')}),
    )
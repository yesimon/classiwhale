import nexus
import os.path

CORSAIR_ROOT = os.path.dirname(__file__)

class CorsairException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CorsairModule(nexus.NexusModule):
    def get_title(self):
        return 'Corsair'

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': os.path.join(CORSAIR_ROOT, 'media'),
                'show_indexes': True,
            }, name='media'),

            url(r''),
        )

        return urlpatterns

    def render_on_dashboard(self, request):
        return self.render_to_string('corsair/nexus/dashboard.html', {},
                                     request)

#nexus.site.register(CorsairModule, 'corsair')

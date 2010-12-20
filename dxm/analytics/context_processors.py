from django.conf import settings

GOOGLE_ANALYTICS_KEY = getattr(settings, 'GOOGLE_ANALYTICS_KEY')

def google_analytics(request):
    return {'GOOGLE_ANALYTICS_KEY': GOOGLE_ANALYTICS_KEY}

from twitter.models import *
import settings

def constants(request):
    return {
               'TEMPLATES': settings.TEMPLATES,
               'CONSTANTS': settings.CONSTANTS,
           }

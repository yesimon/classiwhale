try:
    from settings import *
    DATABASES['default'] = DATABASES['local']
    CONSTANTS['local_js'] = True
except ImportError:
    print("I can't find settings.py!")
    

# Django settings for dxm project.
import os.path
import sys
from glob import glob
ROOT_PROJECT_PATH = os.path.dirname(__file__).replace('\\','/')
for p in glob(os.path.join(ROOT_PROJECT_PATH, '../lib/*')):
    sys.path.insert(0, p)
sys.path.insert(0, os.path.join(ROOT_PROJECT_PATH, '../lsd'))
import djcelery
djcelery.setup_loader()



DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Simon Ye', 'simon@classiwhale.com'),
    ('Dan Huang', 'dan@classiwhale.com'),
    ('Alex Churchill', 'alex@classiwhale.com'),
    ('Emilio Lopez', 'emilio@classiwhale.com'),
    ('Ken Kansky', 'kkansky@classiwhale.com')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'classiwhale',
        'HOST': '109.169.56.133',
        'PORT': '',
        'USER': 'classiwhale',
        'PASSWORD': 'wombocombo',
    },
    'local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_PROJECT_PATH, "localdb.db"),
    },
}

try:
    import socket
    INTERNAL_IPS = (
        socket.gethostbyname(socket.gethostname()),
        '127.0.0.1',
    )
except:
    INTERNAL_IPS = ('127.0.0.1', )

CACHE_BACKEND = 'locmem://'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute root url of the site
ROOT_URL = 'http://www.classiwhale.com'

SERVER_EMAIL = 'server@classiwhale.com'

# Absolute path to the directory that holds media. (this actually means uploaded media?? unsure about this using as regular media for now)
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'


STATIC_DOC_ROOT = os.path.join(ROOT_PROJECT_PATH, 'static')
STATIC_SERVE = True


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=xleed6svvm^c8r(3ufrm6)ke%)f&+38g7t+zluth9=ap7i%gc'

CONSUMER_KEY = 'H3jdfPuU3srfX2uo7LFQ1w'

CONSUMER_SECRET = 'Fe0iHcfi8nubMBzjbcUuf6zRW8Nn9VgMJkiHcCdKwSw'

AUTHENTICATION_BACKENDS = (
    'backends.twitteroauth.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'twitterauth.UserProfile'

# These login urls require the path relative to the direct mount of / on the ip
# address. This is a django restriction.
LOGIN_URL = '/twitterauth/login/'

LOGIN_REDIRECT_URL = '/'

IGNORABLE_404_STARTS = ('/cgi-bin/', '/_vti_bin', '/_vti_inf', '/static/')


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

GOOGLE_ANALYTICS_KEY = False

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "analytics.context_processors.google_analytics",
)


MIDDLEWARE_CLASSES = (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
)

ROOT_URLCONF = 'urls'


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

def always_show_toolbar(request):
    return True # Always show debug toolbar

DEBUG_TOOLBAR_CONFIG = {
#    'SHOW_TOOLBAR_CALLBACK': always_show_toolbar,
    'INTERCEPT_REDIRECTS': False,
}

# Djcelery settings for rabbitmq broker
BROKER_HOST = '109.169.56.133'
BROKER_PORT = 5672
BROKER_USER = 'classiwhale'
BROKER_PASSWORD = 'wombocombo'
BROKER_VHOST = 'magicfilter'



# Devserver settings
DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    #'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    #'devserver.modules.cache.CacheSummaryModule',
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.markup',
    'annoying',
    'compressor',
    'south',
    'djcelery',
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    'sentry.client.celery',
    'picklefield',
    'django_extensions',
    'tastypie',
    'base',
    'twitterauth',
    'backends',
    'feedback',
    'status',
    'search',
    'classifier',
    'multinomialbayes',
)

if DEBUG == True:
    INSTALLED_APPS += (
        'devserver',
#    'debug_toolbar',
    )

# Load local settings for each machine
try:
    from local_settings import *
except ImportError:
    pass

# Django settings for fc3 project.
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = BASE_DIR

ALLOWED_INCLUDE_ROOTS = (BASE_DIR,)
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

ADMINS = (
    ('Graham Ullrich', 'graham@flyingcracker.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
#TIME_ZONE = 'US/Mountain'
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r9o847m+!y4vy6ohegip0d)a95pmbok9y0k@^7)pl#tfhq7zwy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

# List of context processors, with some custom ones at the top.
TEMPLATE_CONTEXT_PROCESSORS = ('fc3.context_processors.yui_version',
                               'fc3.context_processors.miniblog',
                               'fc3.context_processors.system_version',
                               'fc3.context_processors.login_url_with_redirect',
                               'django.contrib.messages.context_processors.messages',
                               'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.debug',
                               'django.core.context_processors.i18n',
                               'django.core.context_processors.media',
                               'django.core.context_processors.request',
                               )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'fc3.urls'

APPEND_SLASH = True

from unipath import FSPath as Path
TEMPLATE_DIRS = (
    Path(__file__).ancestor(2).child("templates"),
    Path(__file__).parent.child("templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django_extensions',
    'django.contrib.flatpages',
    'django.contrib.messages',

    'south',
    'uni_form',
    'registration',
    'django_mailer',
#    'profiles',
    'sms',
    'timezones',

    'scoresys',
    'home',
    'fcprofile',
    'weatherstation',
    'weather',
    'food',
    'blog',
    'cam',
    'miniblog',
    'grill',
    'fantasy',
)

AUTHENTICATION_BACKENDS = (
    "fc3.email-auth.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "cracklyfinger.com"

AUTH_PROFILE_MODULE = 'fcprofile.FCProfile'

# import local settings overriding the defaults
try:
    from settings_local import *
except ImportError:
    try:
        from mod_python import apache
        apache.log_error( "settings_local.py not found!", apache.APLOG_NOTICE )
    except ImportError:
        import sys
        sys.stderr.write( "settings_local.py not found!\n" )

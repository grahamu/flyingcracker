# Django settings for fc3 project.
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = BASE_DIR

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Denver'

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
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'fc3.urls'

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
    'django.contrib.markup',
    'django.contrib.comments',
    'django.contrib.humanize',
    'fc3.django_evolution',
    'fc3.weatherstation',
    'fc3.weather',
    'fc3.food',
    'fc3.blog',
//    'fc3.registration',
    'fc3.cam',
)

AUTHENTICATION_BACKENDS = (
    "email-auth.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)

ACCOUNT_ACTIVATION_DAYS = 10

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gmsearch@flyingcracker.com'
EMAIL_HOST_PASSWORD = 'scalzo'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'graham@flyingcracker.com'

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

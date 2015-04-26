from __future__ import absolute_import
import os
from unipath import Path

from .secrets import get_secret

SECRET_KEY = get_secret('SECRET_KEY')

BASE_DIR = Path(__file__).ancestor(3)

ALLOWED_INCLUDE_ROOTS = (BASE_DIR,)


MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("static_media")
STATICFILES_DIRS = (
    BASE_DIR.child("static"),
)

TEMPLATE_DIRS = (
    BASE_DIR.child("templates"),
    Path(__file__).parent.child("templates"),
)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

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

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django_extensions',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'markup_deprecated',
    'south',
    'uni_form',
    'registration',
    'django_mailer',
#    'profiles',
    'sms',
    'timezones',
    ]

PROJECT_APPS = [
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
    'home',
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

AUTHENTICATION_BACKENDS = (
    "fc3.email-auth.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "cracklyfinger.com"

AUTH_PROFILE_MODULE = 'fcprofile.FCProfile'

ALLOWED_HOSTS = ['www.cracklyfinger.com', 'cracklyfinger.com', '*']

# Email service credentials are secret.
EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 25
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'cracklyfinger@flyingcracker.com'
SERVER_EMAIL = 'graham@flyingcracker.com'

from __future__ import absolute_import
from unipath import Path

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'NAME': 'graham_fc3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'graham_fc3',
        'PASSWORD': '132af5e4',
        'HOST': 'localhost',
    }
}

# Where are media and weather files?
MEDIA_DIR = STATIC_DIR = Path("/home/graham/webapps")
MEDIA_ROOT = MEDIA_DIR.child("media")
WEATHER_ROOT = MEDIA_ROOT.child('weather')
STATIC_ROOT = STATIC_DIR.child('static')

STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)

STATIC_URL = 'http://cracklyfinger.com/static/'
MEDIA_URL = 'http://cracklyfinger.com/media/'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "cracklyfinger.com"

AUTH_PROFILE_MODULE = 'fcprofile.FCProfile'

ALLOWED_HOSTS = ['www.cracklyfinger.com', 'cracklyfinger.com', '*']

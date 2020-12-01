from unipath import Path

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'NAME': 'fc3staging',
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
STATIC_ROOT = STATIC_DIR.child('staging_static')

STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)

STATIC_URL = 'http://ullrichsoftware.com/static/'
MEDIA_URL = 'http://ullrichsoftware.com/media/'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

##EMAIL_USE_TLS = True
##EMAIL_PORT = 587
##DEFAULT_FROM_EMAIL = "John Evans <johnevanswebbot@gmail.com>"

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "ullrichsoftware.com"

AUTH_PROFILE_MODULE = 'fcprofile.FCProfile'

ALLOWED_HOSTS = ['www.ullrichsoftware.com', 'ullrichsoftware.com', '*']

from unipath import Path

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'NAME': 'fc3',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'fc3_graham',
        'PASSWORD': 'PHI-peephole-tavern-aglow',
        'HOST': 'grahamu-1981.postgres.pythonanywhere-services.com',
        'PORT': 11981,
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

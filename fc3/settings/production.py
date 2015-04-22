import os
import sys

from unipath import Path
#!/usr/bin/env python
from .base import *

DEBUG=False

DATABASES = {
    'default': {
        'NAME': 'graham_fc3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'graham_fc3',
        'PASSWORD': '132af5e4',
        'HOST': 'localhost',
    }
}

# This setting describes the URL path where static content originates.
# If in a Django development server environment, this should be 'static'.
# If in a production environment the value will look like 'http://domainname/appname/static'.

BASE_DIR = Path('/home/graham/webapps')

MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child('staging_static')
WEATHER_ROOT = MEDIA_ROOT + '/weather/'

ALLOWED_INCLUDE_ROOTS = (BASE_DIR,)

STATIC_URL = 'http://ullrichsoftware.com/static/'
MEDIA_URL = 'http://ullrichsoftware.com/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR.child('fc3'), 'static'),
    )
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "ullrichsoftware.com"

AUTH_PROFILE_MODULE = 'fcprofile.FCProfile'

ALLOWED_HOSTS = ['www.ullrichsoftware.com', 'ullrichsoftware.com', '*']


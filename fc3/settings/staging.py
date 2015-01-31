from __future__ import absolute_import
import sys

from unipath import Path
#!/usr/bin/env python
from .base import *


import json
secrets = json.load(file("fc3/settings/secrets.json"))
SECRET_KEY = secrets['SECRET_KEY']

DEBUG=True

DATABASES = {
    'default': {
        'NAME': 'fc3staging',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'graham_fc3',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

# This setting describes the URL path where static content originates.
# If in a Django development server environment, this should be 'static'.
# If in a production environment the value will look like 'http://domainname/appname/static'.

BASE_DIR = Path(__file__).ancestor(5)

LOCAL_ROOT = BASE_DIR.child("media")
WEATHER_ROOT = LOCAL_ROOT + '/weather/'

ALLOWED_INCLUDE_ROOTS = (BASE_DIR,)


MEDIA_ROOT = BASE_DIR.child("webapps").child("staging_media")
STATIC_ROOT = BASE_DIR.ancestor(2).child("webapps").child("staging_static")

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

DEFAULT_FROM_EMAIL = "John Evans <johnevanswebbot@gmail.com>"

try:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'johnevanswebbot@gmail.com'
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 587
except:
    print "email not working"


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "ullrichsoftware.com"

AUTH_PROFILE_MODULE = 'fcprofile.FCProfile'

ALLOWED_HOSTS = ['www.ullrichsoftware.com', 'ullrichsoftware.com', '*']
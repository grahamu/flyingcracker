from __future__ import absolute_import
import sys

from unipath import Path
import json
#!/usr/bin/env python
from .local import *


DEBUG=True

DATABASES = {
    'default': {
        'NAME': 'flyingcracker',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'maine',
        'HOST': 'localhost',
    }
}

# This setting describes the URL path where static content originates.
# If in a Django development server environment, this should be 'static'.
# If in a production environment the value will look like 'http://domainname/appname/static'.


LOCAL_URL = 'local'

BASE_DIR = Path(__file__).ancestor(3)

LOCAL_ROOT = BASE_DIR.child("media")

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



INTERNAL_IPS = '127.0.0.1'


# Just dump emails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Set queue time to 0, so mail is sent instantly.
NOTIFICATIONS_QUEUE_MINS = 0
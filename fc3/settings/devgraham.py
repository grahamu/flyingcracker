from __future__ import absolute_import
import sys

from unipath import Path
import json
#!/usr/bin/env python
from .local import *


DEBUG=True

DATABASES = {
    'default': {
        'NAME': 'fc3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'graham',
        'PASSWORD': '',
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

DEFAULT_FROM_EMAIL = "Graham Ullrich <graham@flyingcracker.com>"

try:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'graham@flyingcracker.com'
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 587
except:
    print "email not working"



INTERNAL_IPS = '127.0.0.1'

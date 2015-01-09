import sys

from unipath import Path
import json
#!/usr/bin/env python
from base import *


DEBUG=True

DATABASES = {
    'default': {
        'NAME': 'flyingcracker',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'johnevans',
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
WEATHER_ROOT = LOCAL_ROOT + 'weather/'
 
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

sys.path.insert(0, '/Users/johnevans/venv/flyingcracker/src')
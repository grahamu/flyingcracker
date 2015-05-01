from __future__ import absolute_import
from .local import *

DATABASES = {
    'default': {
        'NAME': 'fc3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'graham',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

LOCAL_ROOT = "/Users/graham/Documents/fc3/testing/web/media"
WEATHER_ROOT = LOCAL_ROOT + '/weather/'

# Just dump emails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Set queue time to 0, so mail is sent instantly.
NOTIFICATIONS_QUEUE_MINS = 0

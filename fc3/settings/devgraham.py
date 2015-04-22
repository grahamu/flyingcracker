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

from .local import *

DATABASES = {
    'default': {
        'NAME': 'graham',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'graham',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

LOCAL_ROOT = Path("/Users/graham/code/flyingcracker/testing/web/media")
WEATHER_ROOT = LOCAL_ROOT + '/weather/'

# Just dump emails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Set queue time to 0, so mail is sent instantly.
NOTIFICATIONS_QUEUE_MINS = 0

# INSTALLED_APPS += [
#    'test_plus',
# ]

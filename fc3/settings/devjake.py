from __future__ import absolute_import

from unipath import Path

from .local import *

DEBUG = True

DATABASES = {
    'default': {
        'NAME': 'flyingcracker',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'johnevans',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

DEFAULT_FROM_EMAIL = "John Evans <johnevanswebbot@gmail.com>"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'johnevanswebbot@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

LOCAL_URL = 'local'

BASE_DIR = Path(__file__).ancestor(3)

LOCAL_ROOT = BASE_DIR.child("media")

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

DEFAULT_FROM_EMAIL = "John Evans <johnevanswebbot@gmail.com>"

# Just dump emails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Set queue time to 0, so mail is sent instantly.
NOTIFICATIONS_QUEUE_MINS = 0

INSTALLED_APPS += [
    test_plus,
]

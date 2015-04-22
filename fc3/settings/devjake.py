from __future__ import absolute_import
from .local import *

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

# Jake, please fix whatever path problem this solves in some other way.
#
# sys.path.insert(0, '/Users/johnevans/venv/flyingcracker/src')
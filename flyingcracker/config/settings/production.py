import os

import dj_database_url
from unipath import Path

from .base import *

DEBUG = False

BASE_DIR = Path(__file__).ancestor(3)

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600),
}

# Read secrets from environment variables on Railway
SECRET_KEY = os.environ["SECRET_KEY"]
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

MEDIA_ROOT = BASE_DIR.child("media")
WEATHER_ROOT = MEDIA_ROOT.child("weather")

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

# Remove silk in production
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ("silk",)]
MIDDLEWARE = tuple(
    m for m in MIDDLEWARE if m != "silk.middleware.SilkyMiddleware"
)

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

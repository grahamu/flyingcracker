from .base import *

DEBUG = True

LOCAL_URL = "local"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOCAL_ROOT = BASE_DIR.parent / "media"
WEATHER_ROOT = LOCAL_ROOT / "weather"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

INTERNAL_IPS = "127.0.0.1"

# Disable cache middleware for development so template changes show immediately.
MIDDLEWARE = tuple(
    m for m in MIDDLEWARE
    if m not in (
        "django.middleware.cache.UpdateCacheMiddleware",
        "django.middleware.cache.FetchFromCacheMiddleware",
    )
)

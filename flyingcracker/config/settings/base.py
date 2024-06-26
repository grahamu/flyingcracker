from unipath import Path

from .secrets import get_secret

SECRET_KEY = get_secret("SECRET_KEY")

BASE_DIR = Path(__file__).ancestor(3)

MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("staticfiles")
STATICFILES_DIRS = (BASE_DIR.child("static"),)

MEDIA_URL = "media/"
STATIC_URL = "static/"

ADMINS = (
    ("Graham Ullrich", "graham@flyingcracker.com"),
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# TIME_ZONE = 'US/Mountain'
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.child("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "fc3.context_processors.yui_version",
                "fc3.context_processors.system_version",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
            ],
        },
    },
]

MIDDLEWARE = (
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
)

ROOT_URLCONF = "config.urls"

APPEND_SLASH = True

PREREQ_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "django_markup",
    "silk",
    # "timezone_field",
]

PROJECT_APPS = [
    "cam",
    "food",
    "home",
    "weather",
    "weatherstation.apps.WeatherStationConfig",
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

AUTHENTICATION_BACKENDS = (
    "fc3.email-auth.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ACCOUNT_ACTIVATION_DAYS = 10

YUI_VERSION = "2.9.0"

SYSTEM_NAME = "cracklyfinger.com"

AUTH_PROFILE_MODULE = "fcprofile.FCProfile"

ALLOWED_HOSTS = ["www.cracklyfinger.com", "cracklyfinger.com", "*"]

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
NOSE_ARGS = [
    "--logging-filter=-django.request",
]

# Email service credentials are secret.
EMAIL_HOST = get_secret("EMAIL_HOST")
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")

EMAIL_PORT = 25
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "cracklyfinger@flyingcracker.com"
SERVER_EMAIL = "graham@flyingcracker.com"

# Silk Profiler
SILKY_PYTHON_PROFILER = True

SILKY_ANALYZE_QUERIES = True  # Set to True to analyze queries
SILKY_AUTHENTICATION = True  # Set to True to restrict access to logged in users
SILKY_AUTHORISATION = True  # Set to True to restrict access to staff users
SILKY_IGNORE_PATHS = ["/ht"]  # Ignore these paths - this is an undocumented setting!
SILKY_MAX_RECORDED_REQUESTS = 10**4  # Store up to 10k requests
SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
SILKY_META = True  # Record and display silky overhead
SILKY_PYTHON_PROFILER = True  # Set to False to use another profiler

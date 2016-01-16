from __future__ import absolute_import
from unipath import Path

from .base import *

DEBUG = True

LOCAL_URL = 'local'

BASE_DIR = Path(__file__).ancestor(3)
LOCAL_ROOT = BASE_DIR.ancestor(2).child("media")
WEATHER_ROOT = LOCAL_ROOT.child("weather")

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

INTERNAL_IPS = '127.0.0.1'
from __future__ import absolute_import
import json
from unipath import Path

from django.core.exceptions import ImproperlyConfigured

SECRETS_DIR = Path(__file__).parent()


with open(SECRETS_DIR.child("secrets.json")) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """
    Get the secret constant or return explicit exception.
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

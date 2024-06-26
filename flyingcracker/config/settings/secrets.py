import json

from django.core.exceptions import ImproperlyConfigured
from unipath import Path

SECRETS_DIR = Path(__file__).parent


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

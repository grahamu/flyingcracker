import json
import os

from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

SECRETS_DIR = Path(__file__).resolve().parent

try:
    with open(SECRETS_DIR / "secrets.json") as f:
        secrets = json.loads(f.read())
except FileNotFoundError:
    secrets = {}


def get_secret(setting, secrets=secrets):
    """
    Get the secret constant or return explicit exception.
    Falls back to environment variables if secrets.json is missing.
    """
    try:
        return secrets[setting]
    except KeyError:
        val = os.environ.get(setting)
        if val is not None:
            return val
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

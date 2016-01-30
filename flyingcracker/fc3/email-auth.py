from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class EmailBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
        except ValidationError:
            return None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user  # xxx
        else:
            return None

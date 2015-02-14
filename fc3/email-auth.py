from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        if validate_email(username):
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        return None
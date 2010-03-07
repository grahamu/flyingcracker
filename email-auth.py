from django.contrib.auth.backends import ModelBackend
try:
    # Django version <= 1.1
    from django.forms.fields import email_re
except ImportError:
    # Django version >= 1.2
    from django.core.validatore import email_re
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        return None
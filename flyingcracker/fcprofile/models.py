from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from timezone_field import TimeZoneField


class FCProfile(models.Model):
    '''
    FlyingCracker user profile.

    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)  # is the user active?
    timezone = TimeZoneField()

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('profiles_profile_detail',
                       kwargs={'username': self.user.username})

    def full_name(self):
        return self.user.get_full_name()

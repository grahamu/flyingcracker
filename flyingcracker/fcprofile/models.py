from timezones.fields import TimeZoneField

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class FCProfile(models.Model):
    '''
    FlyingCracker user profile.

    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)  # is the user active?
    timezone = TimeZoneField()

    def __unicode__(self):
        return u'%s' % self.user

    def get_absolute_url(self):
        return reverse('profiles_profile_detail',
                       kwargs={'username': self.user.username})

    def full_name(self):
        return self.user.get_full_name()

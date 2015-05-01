from django.db import models
from django.contrib.auth.models import User
from timezones.fields import TimeZoneField


class FCProfile(models.Model):
    '''
    FlyingCracker user profile.

    '''
    user = models.OneToOneField(User)
    active = models.BooleanField(default=True)  # is the user active?
    timezone = TimeZoneField()

    def __unicode__(self):
        return u'%s' % self.user

    def get_absolute_url(self):
        return ('profiles_profile_detail', (),
                {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    def full_name(self):
        return self.user.get_full_name()

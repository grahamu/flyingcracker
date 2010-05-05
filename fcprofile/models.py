from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from timezones.fields import TimeZoneField

from django.conf import settings

if 'sms' in settings.INSTALLED_APPS:
    from sms.models import ContentTypePhoneNumber
else:
    ContentTypePhoneNumber = None


class FCProfile(models.Model):
    '''
    FlyingCracker user profile.
    
    '''
    user            = models.OneToOneField(User)
    active          = models.BooleanField(default=True) # is the user active?
    timezone        = TimeZoneField()
        
    def __unicode__(self):
        return u'%s' % self.user

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

    def full_name(self):
        return self.user.get_full_name()

    def get_sms_numbers(self):
        if ContentTypePhoneNumber:
            content_type = ContentType.objects.get_for_model(self)
            try:
                qs = ContentTypePhoneNumber.objects.filter(
                    content_type=content_type,
                    object_id=self.pk,
                    )
            except ContentTypePhoneNumber.DoesNotExist:
                qs = []
        else:
            qs = []
        return qs

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^timezones\.fields\.TimeZoneField"])
except ImportError:
    pass

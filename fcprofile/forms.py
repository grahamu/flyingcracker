#!/usr/bin/env python
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from fcprofile.models import FCProfile

attrs_dict = { 'class': 'required' }


class ProfileForm(forms.ModelForm):
    '''
    Form used for a user to edit their information.
    
    '''
    from django.contrib.localflavor.us.forms import USPhoneNumberField
    
    first_name = forms.CharField(label=_(u'First name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30)
    email = forms.EmailField(label="Primary email")
    mobile = USPhoneNumberField(label=_('SMS mobile'), required=False)
    carrier = forms.ModelChoiceField(label=_(u'Carrier'), queryset=None, required=False)
    
    class Meta:
        model = FCProfile
        exclude = ('user', 'active')
        
    def __init__(self, *args, **kwargs):
        from sms.models import Carrier, ContentTypePhoneNumber
        
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self['carrier'].field.queryset = Carrier.objects.all()
            
            # find existing ContentTypePhoneNumber associated with this instance.
            self.content_type = ContentType.objects.get_for_model(self.instance)
            self.object_id = self.instance.pk
            try:
                self.ctpn = ContentTypePhoneNumber.objects.get(
                    content_type=self.content_type,
                    object_id=self.object_id,
                    )
            except ContentTypePhoneNumber.DoesNotExist:
                self.ctpn = None
            else:
                self.fields['mobile'].initial = self.ctpn.phone_number
                self.fields['carrier'].initial = self.ctpn.carrier.pk
        except User.DoesNotExist:
            pass
        
        self.fields.keyOrder = ['first_name', 'last_name', 'email',
                                'timezone', 'mobile', 'carrier']
        
    def save(self, *args, **kwargs):
        '''
        Update the primary email address on the related User object.
        Update the first name and last name.
        Update the ContentTypePhoneNumber as needed. 
        
        '''
        from sms.models import Carrier, ContentTypePhoneNumber
        
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()

        phone_number = self.cleaned_data['mobile']
        carrier = self.cleaned_data['carrier']
        # If we found an existing ContentTypePhoneNumber, either update the 
        # phone number and carrier if both are entered, or delete the CTPN
        # if either field is blank.
        # Likewise, only create a new ContentTypePhoneNumber if both
        # fields are supplied.
        if self.ctpn:
            if phone_number and carrier:
                self.ctpn.phone_number = phone_number
                self.ctpn.carrier = carrier
                self.ctpn.save()
            else:
                self.ctpn.delete()
        else:
            if phone_number and carrier:
                ctpn = ContentTypePhoneNumber.objects.create(
                    content_type=self.content_type,
                    object_id=self.object_id,
                    carrier=carrier,
                    phone_number=phone_number,
                    )
            
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

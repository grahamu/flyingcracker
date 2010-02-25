#!/usr/bin/env python
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from serviceclient.models import ServiceClientUserProfile

attrs_dict = { 'class': 'required' }


class ProfileForm(forms.ModelForm):
    '''
    Form used for a user to edit their information.
    
    '''
    from django.contrib.localflavor.us.forms import USPhoneNumberField
    
    first_name = forms.CharField(label=_(u'First name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30)
    email = forms.EmailField(label="Primary email")
    
    class Meta:
        model = ServiceClientUserProfile
        exclude = ('user', 'service_client', 'user_type', 'active')
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
        
    def save(self, *args, **kwargs):
        '''
        Update the primary email address on the related User object.
        Update the first name and last name.
        
        '''
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
            
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

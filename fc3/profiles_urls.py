from django.conf.urls.defaults import *
from fcprofile.forms import ProfileForm


# Put these URL patterns first so they match first.

urlpatterns = patterns('',
    url(r'^edit/$', 'profiles.views.edit_profile',
                    {'form_class': ProfileForm, 'success_url': '/'},
                    name='profiles_edit_profile'),
)

# We don't need the other views:

#urlpatterns += profiles_patterns
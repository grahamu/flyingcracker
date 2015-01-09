from __future__ import absolute_import
from django.conf.urls.defaults import *



urlpatterns = patterns('home.views',
    url(r'^$',          'home', name='fc-home'),
    url(r'^about/$',    'about', name='fc-about'),
)

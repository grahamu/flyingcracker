from django.conf.urls import (
    patterns,
    url,
    include,
)


app_name = 'home'
urlpatterns = patterns('home.views',
    url(r'^$',          'home', name='fc-home'),
    url(r'^about/$',    'about', name='fc-about'),
)

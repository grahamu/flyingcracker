from django.conf.urls import patterns, url, include



urlpatterns = patterns('home.views',
    url(r'^$',          'home', name='fc-home'),
    url(r'^about/$',    'about', name='fc-about'),
)

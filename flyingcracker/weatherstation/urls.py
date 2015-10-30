from django.conf.urls import (
    patterns,
    url,
)


app_name = 'weatherstation'
urlpatterns = patterns('weatherstation.views',
    url(r'^upload/$', 'upload_data', name='weatherstation-upload'),
    url(r'^$', 'download_data', name='weatherstation-download'),
)

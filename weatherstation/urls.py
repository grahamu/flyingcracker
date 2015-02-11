from django.conf.urls import patterns, url, include

urlpatterns = patterns('weatherstation.views',
    (r'^upload/$', 'upload_data'),
    (r'^$', 'download_data'),
)

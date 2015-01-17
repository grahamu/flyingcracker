from django.conf.urls.defaults import *

urlpatterns = patterns('weatherstation.views',
    (r'^upload/$', 'upload_data'),
    (r'^$', 'download_data'),
)

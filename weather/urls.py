from django.conf.urls.defaults import *

urlpatterns = patterns('fc3.weather.views',
    (r'^current/$',     'current'),
    (r'^unitchange/$',  'unit_change'),
    url(r'^$',          'weather', name='fc-weather'),
    url(r'^generate/$', 'generate', name='generate-weather'),
    url(r'^delete/$',   'delete', name='delete-weather'),
    url(r'^data/$',     'output_data', name='output-data'),
    url(r'^chart/$',    'chart', name='weather-chart'),
)

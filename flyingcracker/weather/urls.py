from django.conf.urls import (
    patterns,
    url,
)


app_name = 'weather'
urlpatterns = patterns('weather.views',
    url(r'^current/$',     'current', name='weather-current'),
    url(r'^unitchange/$',  'unit_change', name='weather-unit-change'),
    url(r'^$',          'weather', name='weather-root'),
    url(r'^generate/$', 'generate', name='weather-generate'),
    url(r'^delete/$',   'delete', name='weather-delete'),
    url(r'^data/$',     'output_data', name='weather-data'),
    url(r'^chart/$',    'chart', name='weather-chart'),
)

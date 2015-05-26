from django.conf.urls import patterns, url

urlpatterns = patterns('weather.views',
    url(r'^current/$',     'current', name='weather-current'),
    url(r'^unitchange/$',  'unit_change', name='weather-unit-change'),
    url(r'^$',          'weather', name='weather-root'),
    url(r'^generate/$', 'generate', name='generate-weather'),
    url(r'^delete/$',   'delete', name='delete-weather'),
    url(r'^data/$',     'output_data', name='output-data'),
    url(r'^chart/$',    'chart', name='weather-chart'),
)

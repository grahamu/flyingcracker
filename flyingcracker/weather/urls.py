from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^current/$', views.current, name='weather-current'),
    url(r'^unitchange/$', views.unit_change, name='weather-unit-change'),
    url(r'^$', views.weather, name='weather-root'),
    url(r'^generate/$', views.generate, name='generate-weather'),
    url(r'^delete/$', views.delete, name='delete-weather'),
    url(r'^data/$', views.output_data, name='output-data'),
    url(r'^chart/$', views.chart, name='weather-chart'),
]

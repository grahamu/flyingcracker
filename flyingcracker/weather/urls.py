from django.conf.urls import url

from . import views

app_name = 'weather'
urlpatterns = [
    url(r'^current/$', views.current, name='weather-current'),
    url(r'^unitchange/$', views.unit_change, name='weather-unit-change'),
    url(r'^$', views.weather, name='weather-root'),
    url(r'^generate/$', views.generate, name='weather-generate'),
    url(r'^delete/$', views.delete, name='weather-delete'),
    url(r'^data/$', views.output_data, name='weather-data'),
    url(r'^chart/$', views.chart, name='weather-chart'),
]

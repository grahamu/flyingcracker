from django.conf.urls import url

from . import views

app_name = 'weather'
urlpatterns = [
    url(r'^$', views.weather, name='root'),
    url(r'^current/$', views.current, name='current'),
    url(r'^unitchange/$', views.unit_change, name='unit-change'),
    url(r'^generate/$', views.generate, name='generate'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^data/$', views.output_data, name='data'),
    url(r'^chart/$', views.chart, name='chart'),
]

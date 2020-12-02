from django.urls import re_path

from . import views

app_name = 'weather'
urlpatterns = [
    re_path(r'^$', views.weather, name='root'),
    re_path(r'^current/$', views.current, name='current'),
    re_path(r'^unitchange/$', views.unit_change, name='unit-change'),
    re_path(r'^generate/$', views.generate, name='generate'),
    re_path(r'^delete/$', views.delete, name='delete'),
    re_path(r'^data/$', views.output_data, name='data'),
    re_path(r'^chart/$', views.chart, name='chart'),
]

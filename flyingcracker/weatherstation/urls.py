from django.urls import re_path

from . import views

app_name = 'weatherstation'
urlpatterns = [
    re_path(r'^upload/$', views.upload_data, name='upload'),
]

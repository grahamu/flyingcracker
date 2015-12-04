from django.conf.urls import url

from . import views

app_name = 'weatherstation'
urlpatterns = [
    url(r'^upload/$', views.upload_data, name='upload'),
]

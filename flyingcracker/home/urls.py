from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.home, name='fc-home'),
    url(r'^about/$', views.about, name='fc-about'),
]

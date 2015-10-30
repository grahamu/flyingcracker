from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='fc-home'),
    url(r'^about/$', views.about, name='fc-about'),
]

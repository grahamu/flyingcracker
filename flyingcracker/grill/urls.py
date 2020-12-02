from django.urls import re_path

from . import views

app_name = 'grill'
urlpatterns = [
    re_path(r'^d/(?P<slug>[\w_-]+)/$', views.doneness_detail, name='doneness-detail'),
    re_path(r'^$', views.grill, name='grill'),
]

from django.urls import re_path

from . import views

app_name = 'cam'
urlpatterns = [
    re_path(r'^$', views.cam_view, name='root'),
    re_path(r'^list/$', views.cam_list, name='list'),
    re_path(r'^image/$', views.cam_image, name='image'),
]

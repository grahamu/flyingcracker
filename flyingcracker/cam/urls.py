from django.conf.urls import url

from . import views

app_name = 'cam'
urlpatterns = [
    url(r'^$', views.cam_view, name='root'),
    url(r'^list/$', views.cam_list, name='list'),
    url(r'^image/$', views.cam_image, name='image'),
]

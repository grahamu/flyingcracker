from django.conf.urls import url

from . import views

app_name = 'cam'
urlpatterns = [
    url(r'^$', views.cam_view, name='cam-root'),
    url(r'^list/$', views.cam_list, name='cam-list'),
    url(r'^image/$', views.cam_image, name='cam-image'),
]

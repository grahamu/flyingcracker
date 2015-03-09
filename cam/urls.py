from django.conf.urls import patterns, url, include
from django.contrib import admin


urlpatterns = patterns('cam.views',
    url(r'^list/$',            'cam_list', name='cam-list'),
    url(r'^image/$',           'cam_image', name='cam-image'),
    url(r'^$',                 'cam_view', name='cam-root'),
)

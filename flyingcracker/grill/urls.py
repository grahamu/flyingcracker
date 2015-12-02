from django.conf.urls import url

from . import views

app_name = 'grill'
urlpatterns = [
    url(r'^d/(?P<slug>[\w_-]+)/$', views.doneness_detail,
        name='grill-doneness-detail'),
    url(r'^$', views.grill,
        name='grill'),
]

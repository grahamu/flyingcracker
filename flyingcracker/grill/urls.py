from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^d/(?P<slug>[\w_-]+)/$', views.doneness_detail,
        name='grill-doneness-detail'),
    url(r'^$', views.grill,
        name='grill'),
]

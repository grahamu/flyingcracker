from __future__ import absolute_import

from django.conf.urls import url
from django.views.generic import dates

from . import views
from .models import Post

app_name = 'miniblog'
urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
        dates.DateDetailView.as_view,
        {'model': Post, 'date_field': 'pub_date'},
        name='miniblog-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
        dates.DayArchiveView.as_view, {'model': Post}),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        dates.MonthArchiveView.as_view, {'model': Post}),
    url(r'^(?P<year>\d{4})/$',
        dates.YearArchiveView.as_view, {'model': Post}),
    url(r'^$',
        dates.ArchiveIndexView.as_view,
        {'model': Post, 'date_field': 'pub_date'},
        name='miniblog-archive'),
]

urlpatterns += [
    url(r'^special/$', views.special,  name='miniblog-special')
]

from __future__ import absolute_import
from django.conf.urls.defaults import *
from django.views.generic import dates

from .models import Post

urlpatterns = patterns('',
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/(?P<slug>[0-9A-Za-z-]+)/$',
     dates.DateDetailView.as_view(model=Post, date_field='pub_date')),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$',
     dates.DayArchiveView.as_view(model=Post)),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
     dates.MonthArchiveView.as_view(model=Post)),
    (r'^(?P<year>\d{4})/$',
     dates.YearArchiveView.as_view(model=Post)),
    url(r'^$',
        dates.ArchiveIndexView.as_view(model=Post, date_field='pub_date'), name='fc-blog'),
)

urlpatterns += patterns('blog.views',
    (r'^upload/$',  'upload_file'),
 )
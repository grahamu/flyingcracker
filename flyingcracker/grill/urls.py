from django.conf.urls import patterns, url, include

urlpatterns = patterns('grill.views',
    url(r'^d/(?P<slug>[\w_-]+)/$',      'doneness_detail', name='grill-doneness-detail'),
    url(r'^$',                          'grill', name='grill'),
)


#!/usr/bin/env python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.root,
        name='fantasy-root'),
    url(r'^series/add/$', views.series_edit,
        name='fantasy-series-add'),
    url(r'^series/(?P<id>[0-9]+)/$', views.series_dashboard,
        name='fantasy-series-home'),
    url(r'^series/(?P<id>[0-9]+)/edit/$', views.series_edit,
        name='fantasy-series-edit'),
    url(r'^series/(?P<id>[0-9]+)/leaderboard/$', views.leaderboard,
        name='fantasy-series-leaderboard'),
    url(r'^series/(?P<id>[0-9]+)/email/$', views.series_email,
        name='fantasy-series-email'),

    url(r'^series/(?P<id>[0-9]+)/competitor/list/$', views.competitor_list,
        name='fantasy-competitor-list'),
    url(r'^series/(?P<id>[0-9]+)/competitor/export/$', views.competitor_export,
        name='fantasy-competitor-export'),
    url(r'^series/(?P<id>[0-9]+)/competitor/import/$', views.competitor_import,
        name='fantasy-competitor-import'),
    url(r'^competitor/(?P<id>[0-9]+)/edit/$', views.competitor_edit,
        name='fantasy-competitor-edit'),
    url(r'^competitor/(?P<id>[0-9]+)/delete/$', views.competitor_delete,
        name='fantasy-competitor-delete'),

    url(r'^series/(?P<series_id>[0-9]+)/event/add/$', views.event_add,
        name='fantasy-event-add'),
    url(r'^event/(?P<id>[0-9]+)/$', views.event_detail,
        name='fantasy-event-detail'),
    url(r'^event/(?P<id>[0-9]+)/edit/$', views.event_edit,
        name='fantasy-event-edit'),
    url(r'^event/(?P<id>[0-9]+)/delete/$', views.event_delete,
        name='fantasy-event-delete'),
    url(r'^event/(?P<id>[0-9]+)/result/$', views.event_result,
        name='fantasy-event-result'),
    url(r'^event/(?P<id>[0-9]+)/result/edit/$', views.result_edit,
        name='fantasy-result-edit'),

    url(r'^series/(?P<series_id>[0-9]+)/team/list/$', views.team_list,
        name='fantasy-team-list'),
    url(r'^series/(?P<series_id>[0-9]+)/team/add/$', views.team_add,
        name='fantasy-team-add'),
    url(r'^team/(?P<id>[0-9]+)/$', views.team_detail,
        name='fantasy-team-detail'),
    url(r'^team/(?P<id>[0-9]+)/edit/$', views.team_edit,
        name='fantasy-team-edit'),
    url(r'^team/(?P<id>[0-9]+)/delete/$', views.team_delete,
        name='fantasy-team-delete'),

]

#!/usr/bin/env python
from django.conf.urls import patterns, url, include

urlpatterns = patterns('fantasy.views',
    url(r'^$',                                      'root', name='fantasy-root'),
    url(r'^series/add/$',                           'series_edit', name='fantasy-series-add'),
    url(r'^series/(?P<id>[0-9]+)/$',                'series_dashboard', name='fantasy-series-home'),
    url(r'^series/(?P<id>[0-9]+)/edit/$',           'series_edit', name='fantasy-series-edit'),
    url(r'^series/(?P<id>[0-9]+)/leaderboard/$',    'leaderboard', name='fantasy-series-leaderboard'),
    url(r'^series/(?P<id>[0-9]+)/email/$',          'series_email', name='fantasy-series-email'),
    
    
    url(r'^series/(?P<id>[0-9]+)/competitor/list/$',   'competitor_list', name='fantasy-competitor-list'),
    url(r'^series/(?P<id>[0-9]+)/competitor/export/$', 'competitor_export', name='fantasy-competitor-export'),
    url(r'^series/(?P<id>[0-9]+)/competitor/import/$', 'competitor_import', name='fantasy-competitor-import'),
    url(r'^competitor/(?P<id>[0-9]+)/edit/$',          'competitor_edit', name='fantasy-competitor-edit'),
    url(r'^competitor/(?P<id>[0-9]+)/delete/$',        'competitor_delete', name='fantasy-competitor-delete'),

    url(r'^series/(?P<series_id>[0-9]+)/event/add/$','event_add', name='fantasy-event-add'),
    url(r'^event/(?P<id>[0-9]+)/$',                  'event_detail', name='fantasy-event-detail'),
    url(r'^event/(?P<id>[0-9]+)/edit/$',             'event_edit', name='fantasy-event-edit'),
    url(r'^event/(?P<id>[0-9]+)/delete/$',           'event_delete', name='fantasy-event-delete'),
    url(r'^event/(?P<id>[0-9]+)/result/$',           'event_result', name='fantasy-event-result'),
    url(r'^event/(?P<id>[0-9]+)/result/edit/$',      'result_edit', name='fantasy-result-edit'),

    url(r'^series/(?P<series_id>[0-9]+)/team/list/$','team_list', name='fantasy-team-list'),
    url(r'^series/(?P<series_id>[0-9]+)/team/add/$', 'team_add', name='fantasy-team-add'),
    url(r'^team/(?P<id>[0-9]+)/$',                   'team_detail', name='fantasy-team-detail'),
    url(r'^team/(?P<id>[0-9]+)/edit/$',              'team_edit', name='fantasy-team-edit'),
    url(r'^team/(?P<id>[0-9]+)/delete/$',            'team_delete', name='fantasy-team-delete'),

)

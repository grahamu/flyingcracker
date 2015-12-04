from django.conf.urls import url

from . import views

app_name = 'fantasy'
urlpatterns = [
    url(r'^$', views.root,
        name='root'),
    url(r'^series/add/$', views.series_edit,
        name='series-add'),
    url(r'^series/(?P<id>[0-9]+)/$', views.series_dashboard,
        name='series-home'),
    url(r'^series/(?P<id>[0-9]+)/edit/$', views.series_edit,
        name='series-edit'),
    url(r'^series/(?P<id>[0-9]+)/leaderboard/$', views.leaderboard,
        name='series-leaderboard'),
    url(r'^series/(?P<id>[0-9]+)/email/$', views.series_email,
        name='series-email'),

    url(r'^series/(?P<id>[0-9]+)/competitor/list/$', views.competitor_list,
        name='competitor-list'),
    url(r'^series/(?P<id>[0-9]+)/competitor/export/$', views.competitor_export,
        name='competitor-export'),
    url(r'^series/(?P<id>[0-9]+)/competitor/import/$', views.competitor_import,
        name='competitor-import'),
    url(r'^competitor/(?P<id>[0-9]+)/edit/$', views.competitor_edit,
        name='competitor-edit'),
    url(r'^competitor/(?P<id>[0-9]+)/delete/$', views.competitor_delete,
        name='competitor-delete'),

    url(r'^series/(?P<series_id>[0-9]+)/event/add/$', views.event_add,
        name='event-add'),
    url(r'^event/(?P<id>[0-9]+)/$', views.event_detail,
        name='event-detail'),
    url(r'^event/(?P<id>[0-9]+)/edit/$', views.event_edit,
        name='event-edit'),
    url(r'^event/(?P<id>[0-9]+)/delete/$', views.event_delete,
        name='event-delete'),
    url(r'^event/(?P<id>[0-9]+)/result/$', views.event_result,
        name='event-result'),
    url(r'^event/(?P<id>[0-9]+)/result/edit/$', views.result_edit,
        name='result-edit'),

    url(r'^series/(?P<series_id>[0-9]+)/team/list/$', views.team_list,
        name='team-list'),
    url(r'^series/(?P<series_id>[0-9]+)/team/add/$', views.team_add,
        name='team-add'),
    url(r'^team/(?P<id>[0-9]+)/$', views.team_detail,
        name='team-detail'),
    url(r'^team/(?P<id>[0-9]+)/edit/$', views.team_edit,
        name='team-edit'),
    url(r'^team/(?P<id>[0-9]+)/delete/$', views.team_delete,
        name='team-delete'),

]

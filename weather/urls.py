from django.urls import path

from . import views

app_name = "weather"
urlpatterns = [
    path("", views.weather, name="root"),
    path("chartdata/", views.chartdata, name="chartdata"),
    path("unitchange/", views.unit_change, name="unit-change"),
    path("set-zone/", views.set_zone, name="set-zone"),
    path("set-river-gauge/", views.set_river_gauge, name="set-river-gauge"),
    path("generate/", views.generate, name="generate"),
    path("delete/", views.delete, name="delete"),
]

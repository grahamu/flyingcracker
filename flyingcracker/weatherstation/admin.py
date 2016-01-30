#!/usr/bin/env python
from django.contrib import admin

from . import models as weatherstation


class WeatherAdmin(admin.ModelAdmin):
    pass

admin.site.register(weatherstation.Weather, WeatherAdmin)

#!/usr/bin/env python
from django.contrib import admin

from . import models as weather


class ChartUrlAdmin(admin.ModelAdmin):
    pass


admin.site.register(weather.ChartUrl, ChartUrlAdmin)

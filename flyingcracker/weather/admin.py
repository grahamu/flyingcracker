#!/usr/bin/env python
from django.contrib import admin
import weather.models as weather


class ChartUrlAdmin(admin.ModelAdmin):
    pass

admin.site.register(weather.ChartUrl, ChartUrlAdmin)


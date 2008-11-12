#!/usr/bin/env python
from django.contrib import admin
from django.contrib.contenttypes import generic
import fc3.grill.models as grill

admin.site.register(grill.Doneness)
admin.site.register(grill.Method)
admin.site.register(grill.Food)
admin.site.register(grill.Hardware)
admin.site.register(grill.Cut)


class GrillingAdmin(admin.ModelAdmin):
    fields = ('food', 'cut', 'doneness', 'method', 'details', 'hardware', 'user')

admin.site.register(grill.Grilling, GrillingAdmin)

#!/usr/bin/env python
from django.contrib import admin

from . import models as grill


class DonenessAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(grill.Doneness, DonenessAdmin)

admin.site.register(grill.Method)
admin.site.register(grill.Food)
admin.site.register(grill.Hardware)
admin.site.register(grill.Cut)


class GrillingAdmin(admin.ModelAdmin):
    fields = ('food', 'cut', 'doneness',
              'method', 'details', 'hardware', 'user')

admin.site.register(grill.Grilling, GrillingAdmin)

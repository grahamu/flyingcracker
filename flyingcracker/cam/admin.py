#!/usr/bin/env python
from django.contrib import admin
import cam.models as cam


class CamAdmin(admin.ModelAdmin):
    
    list_filter = ('category', 'state')

    class Admin:
        fieldset = (
            (None, {'fields': ('title', 'url', 'category', 'description', 'state')}),
        )

admin.site.register(cam.Category)
admin.site.register(cam.Cam, CamAdmin)

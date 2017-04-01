#!/usr/bin/env python
from django.contrib import admin

from . import models as miniblog


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(miniblog.Post, PostAdmin)

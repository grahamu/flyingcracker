#!/usr/bin/env python
from django.contrib import admin

from . import models as scoresys

admin.site.register(scoresys.ScoringSystem)
admin.site.register(scoresys.ResultPoints)

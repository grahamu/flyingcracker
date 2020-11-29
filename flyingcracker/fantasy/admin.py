#!/usr/bin/env python
from django.contrib import admin

from . import models as fantasy


class GuessAdmin(admin.ModelAdmin):
    list_display = ('user', 'competitor', 'late_entry', 'timestamp')
    list_display_links = ('competitor',)
    list_filter = ('user', 'late_entry', 'timestamp')
    list_editable = ('late_entry',)

    # def series(self, obj):
    #     return "%s" % obj.guess_for.series.__unicode__()
    # series.verbose_name = 'series'

    # def event(self, obj):
    #    return "%s" % obj.guess_for.__unicode__()
    # event.verbose_name = 'event'

    def competitor(self, obj):
        return "%s" % obj.competitor

    competitor.short_description = 'Guess'


admin.site.register(fantasy.Guess, GuessAdmin)


class EventAdmin(admin.ModelAdmin):
    list_filter = ('series',)


admin.site.register(fantasy.Event, EventAdmin)
admin.site.register(fantasy.Series)
admin.site.register(fantasy.Competitor)
admin.site.register(fantasy.Result)
admin.site.register(fantasy.Team)

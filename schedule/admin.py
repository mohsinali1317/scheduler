#! -*- coding: utf-8 -*-
from django.contrib import admin

from schedule.models import Division, Team, Ground, Schedule


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'division', 'location']


admin.site.register(Division)
admin.site.register(Team, TeamAdmin)
admin.site.register(Ground)
admin.site.register(Schedule)

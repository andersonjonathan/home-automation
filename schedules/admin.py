from django.contrib import admin

from schedules.models import ScheduleSlot, Schedule


class ScheduleSlotAdmin(admin.StackedInline):
    model = ScheduleSlot


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    inlines = [ScheduleSlotAdmin]

admin.site.register(Schedule, ScheduleAdmin)

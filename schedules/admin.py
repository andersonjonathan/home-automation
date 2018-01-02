from django.contrib import admin

from schedules.models import ScheduleSlot, Schedule


class ScheduleSlotAdmin(admin.StackedInline):
    model = ScheduleSlot
    extra = 0


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    readonly_fields = ('disable_until', 'last_action')
    inlines = [ScheduleSlotAdmin]
    list_display = ('device', 'room')
    list_display_links = ('device',)
    search_fields = ['device']

    def room(self, obj):
        return obj.device.child.room if obj.device else '-'

    class Media:
        js = ('schedules/admin/schedule.js',)
        css = {'all': ('schedules/admin/schedule.css',)}


admin.site.register(Schedule, ScheduleAdmin)

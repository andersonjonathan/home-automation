# from django.contrib import admin
# from .models import (
#     Schedule,
#     ScheduleSlot,
#     Plug,
#     RadioTransmitter,
#     RadioProtocol,
#     RadioSignal,
#     RadioPlug,
#     WiredPlug,
#     Button, WiredButton, RadioButton)
#
#
# class ScheduleSlotAdmin(admin.StackedInline):
#     model = ScheduleSlot
#
#
# class ScheduleAdmin(admin.ModelAdmin):
#     model = Schedule
#     inlines = [ScheduleSlotAdmin]
#
#
# class ButtonAdmin(admin.TabularInline):
#     model = Button
#
#
# class PlugAdmin(admin.ModelAdmin):
#     model = Plug
#
#     inlines = [ButtonAdmin]
#     list_display = ('name',)
#     list_display_links = ('name',)
#     search_fields = ['name']
#
#
# class WiredButtonAdmin(ButtonAdmin):
#     model = WiredButton
#
#
# class WiredPlugAdmin(PlugAdmin):
#     model = WiredPlug
#     inlines = [WiredButtonAdmin]
#
#
# class RadioButtonAdmin(ButtonAdmin):
#     model = RadioButton
#
#
# class RadioPlugAdmin(PlugAdmin):
#     model = RadioPlug
#     inlines = [RadioButtonAdmin]
#
#
#
# admin.site.register(Schedule, ScheduleAdmin)
# admin.site.register(RadioTransmitter)
# admin.site.register(RadioProtocol, RadioProtocolAdmin)
# admin.site.register(RadioPlug, RadioPlugAdmin)
# admin.site.register(WiredPlug, WiredPlugAdmin)
#
# # Register your models here.

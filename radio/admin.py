from django.contrib import admin

from radio.models import RadioTransmitter, Device, Button, RadioProtocol, RadioSignal, RadioCode


class RadioButtonAdmin(admin.TabularInline):
    model = Button


class DeviceAdmin(admin.ModelAdmin):
    model = Device
    inlines = [RadioButtonAdmin]
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']


class RadioSignalAdmin(admin.TabularInline):
    model = RadioSignal


class RadioProtocolAdmin(admin.ModelAdmin):
    model = RadioProtocol

    inlines = [RadioSignalAdmin]
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']

admin.site.register(RadioTransmitter)
admin.site.register(RadioCode)
admin.site.register(RadioProtocol, RadioProtocolAdmin)
admin.site.register(Device, DeviceAdmin)

from django.contrib import admin

from radio.models import RadioTransmitter, Device, Button, RadioProtocol, RadioSignal, RadioCode


class RadioButtonAdmin(admin.TabularInline):
    model = Button


class DeviceAdmin(admin.ModelAdmin):
    model = Device
    inlines = [RadioButtonAdmin]
    list_display = ('name', 'room')
    list_display_links = ('name',)
    search_fields = ['name']


class RadioSignalAdmin(admin.TabularInline):
    model = RadioSignal


class RadioCodeAdmin(admin.ModelAdmin):
    model = RadioCode
    list_display = ('name', 'payload', 'transmitter', 'protocol')
    list_display_links = ('name',)
    search_fields = ['name']


class RadioProtocolAdmin(admin.ModelAdmin):
    model = RadioProtocol

    inlines = [RadioSignalAdmin]
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']


admin.site.register(RadioTransmitter)
admin.site.register(RadioCode, RadioCodeAdmin)
admin.site.register(RadioProtocol, RadioProtocolAdmin)
admin.site.register(Device, DeviceAdmin)

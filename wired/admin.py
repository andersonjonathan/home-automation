from django.contrib import admin
from .models import Device, Button


class ButtonAdmin(admin.TabularInline):
    model = Button


class DeviceAdmin(admin.ModelAdmin):
    model = Device

    inlines = [ButtonAdmin]
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']


admin.site.register(Device, DeviceAdmin)

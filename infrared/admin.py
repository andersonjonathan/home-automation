from django.contrib import admin

# Register your models here.
from .models import Button, Device, Config


class ButtonAdmin(admin.TabularInline):
    model = Button


class DeviceAdmin(admin.ModelAdmin):
    model = Device

    inlines = [ButtonAdmin]
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']


admin.site.register(Device, DeviceAdmin)
admin.site.register(Config)

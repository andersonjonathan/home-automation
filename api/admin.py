from django.contrib import admin

# Register your models here.
from .models import Button, Device


class ButtonAdmin(admin.StackedInline):
    model = Button
    extra = 0


class DeviceAdmin(admin.ModelAdmin):
    model = Device

    inlines = [ButtonAdmin]
    list_display = ('name', 'room')
    list_display_links = ('name',)
    search_fields = ['name']


admin.site.register(Device, DeviceAdmin)

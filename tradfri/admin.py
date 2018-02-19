from django.contrib import admin
from .models import Button, Device, Gateway, TradfriLight


class GatewayAdmin(admin.ModelAdmin):
    model = Gateway
    readonly_fields = ('identity', 'psk')


class TradfriLightAdmin(admin.ModelAdmin):
    model = TradfriLight
    readonly_fields = ('gateway', 'name', 'light_id')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Button)
admin.site.register(Device)
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(TradfriLight, TradfriLightAdmin)

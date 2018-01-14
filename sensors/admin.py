from django.contrib import admin

# Register your models here.
from .models import DHT11, CapacitorDevice, W1Therm, MCP3008, MCP3008Channel, Readings

admin.site.register(DHT11)
admin.site.register(CapacitorDevice)
admin.site.register(W1Therm)
admin.site.register(MCP3008)
admin.site.register(MCP3008Channel)
admin.site.register(Readings)
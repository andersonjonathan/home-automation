from django.contrib import admin

# Register your models here.
from .models import DHT11, CapacitorDevice, W1Therm

admin.site.register(DHT11)
admin.site.register(CapacitorDevice)
admin.site.register(W1Therm)

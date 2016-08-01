from django.contrib import admin

# Register your models here.
from .models import DHT11, CapacitorDevice

admin.site.register(DHT11)
admin.site.register(CapacitorDevice)

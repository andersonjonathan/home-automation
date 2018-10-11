from django.contrib import admin
from .models import Device, Trait, NickName, OnOff

admin.site.register(Device)
admin.site.register(Trait)
admin.site.register(NickName)
admin.site.register(OnOff)

from django.core.management.base import BaseCommand
from sensors.models import DHT11, CapacitorDevice, W1Therm, MCP3008Channel, Readings


class Command(BaseCommand):
    help = 'Checks schedule and performs internal action.'

    def handle(self, *args, **options):
        for device in DHT11.objects.all():
            temp = device.temperature
            hum = device.humidity
            device.last_temperature = temp
            device.last_humidity = hum
            device.save()
            if device.save_temperature:
                Readings(identity="DHT11-{}-temp".format(device.pk), value=temp).save()
            if device.save_humidity:
                Readings(identity="DHT11-{}-hum".format(device.pk), value=hum).save()
        for device in CapacitorDevice.objects.all():
            value = device.value
            device.last_value = value
            device.save()
            if device.save_value:
                Readings(identity="CapacitorDevice-{}".format(device.pk), value=value).save()
        for device in W1Therm.objects.all():
            if device.save_temperature:
                Readings(identity="W1Therm-{}".format(device.pk), value=device.temperature).save()
        for device in MCP3008Channel.objects.all():
            if device.save_value:
                Readings(identity="MCP3008Channel-{}".format(device.pk), value=device.value).save()


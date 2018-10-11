from common.models import BaseDevice, BaseButton
from django.db import models


class Device(models.Model):
    device = models.ForeignKey(BaseDevice, related_name="google_device", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=(
        ("action.devices.types.LIGHT", "LIGHT"),
        ("action.devices.types.OUTLET", "OUTLET"),
        # ("action.devices.types.SCENE", "SCENE"),
        # ("action.devices.types.SWITCH", "SWITCH"),
        # ("action.devices.types.THERMOSTAT", "THERMOSTAT"),
    ))
    name = models.CharField(max_length=255)
    willReportState = models.BooleanField(default=False)
    roomHint = models.CharField(max_length=255)

    def __str__(self):
        return str(self.device)

    def as_dict(self):
        return {
            "id": self.pk,
            "type": self.type,
            "traits": list(self.traits.all().values_list('trait', flat=True)),
            "name": {
                "name": self.name,
                "nicknames": list(self.nicknames.all().values_list('name', flat=True)),
            },
            "willReportState": self.willReportState,
            "roomHint": self.device.child.room.name,
        }

    def get_status(self):
        response = {
            "online": True,
        }
        try:
            response["on"] = self.onoff.on.child.active
        except:
            pass
        return response


class Trait(models.Model):
    trait = models.CharField(max_length=255, choices=(
        # ("action.devices.traits.Brightness", "Brightness"),
        # ("action.devices.traits.CameraStream", "CameraStream"),
        # ("action.devices.traits.ColorSpectrum", "ColorSpectrum"),
        # ("action.devices.traits.ColorTemperature", "ColorTemperature"),
        # ("action.devices.traits.Dock", "Dock"),
        # ("action.devices.traits.FanSpeed", "FanSpeed"),
        # ("action.devices.traits.Locator", "Locator"),
        # ("action.devices.traits.Modes", "Modes"),
        ("action.devices.traits.OnOff", "OnOff"),
        # ("action.devices.traits.RunCycle", "RunCycle"),
        # ("action.devices.traits.Scene", "Scene"),
        # ("action.devices.traits.StartStop", "StartStop"),
        # ("action.devices.traits.TemperatureControl", "TemperatureControl"),
        # ("action.devices.traits.TemperatureSetting", "TemperatureSetting"),
        # ("action.devices.traits.Toggles", "Toggles")
    ))
    device = models.ForeignKey(Device, related_name="traits", on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(str(self.device), self.trait)


class NickName(models.Model):
    name = models.CharField(max_length=255)
    device = models.ForeignKey(Device, related_name="nicknames", on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(str(self.device), self.name)


class OnOff(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, unique=True)
    on = models.ForeignKey(BaseButton, related_name="google_on", on_delete=models.CASCADE)
    off = models.ForeignKey(BaseButton, related_name="google_off", on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(str(self.device))

from django.db import models

from common.models import BaseDevice, BaseButton
from .utils import set_state


class Device(BaseDevice):
    name = models.CharField(max_length=255)
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    parent = models.OneToOneField(BaseDevice, related_name="wired", parent_link=True)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class Button(BaseButton):
    payload = models.CharField(max_length=1, choices=(("0", "0"), ("1", "1")))
    name = models.CharField(max_length=255)
    device = models.ForeignKey(Device, related_name='buttons')
    color = models.CharField(max_length=255, choices=(
        ("btn-default", "White"),
        ("btn-primary", "Blue"),
        ("btn-success", "Green"),
        ("btn-info", "Light blue"),
        ("btn-warning", "Orange"),
        ("btn-danger", "Red"),
    ), default="btn-default")
    priority = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseButton, related_name="wired", parent_link=True)

    def perform_action_internal(self):
        set_state(self.device.gpio, int(self.payload))

    def perform_action(self):
        self.active = True
        for b in self.device.buttons.all():
            if b.name != self.name:
                b.active = False
                b.save()
        self.save()
        self.perform_action_internal()

    def __unicode__(self):
        return u'{name}'.format(name=self.name)

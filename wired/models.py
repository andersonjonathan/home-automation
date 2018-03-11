

from django.db import models

from common.models import BaseDevice, BaseButton, Room
from .utils import set_state


class Device(BaseDevice):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, null=True, blank=True, related_name='wired', on_delete=models.CASCADE)
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    hide_schedule = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseDevice, related_name="wired", parent_link=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{name}{room}'.format(name=self.name, room=', ' + self.room.name if self.room else '')


class Button(BaseButton):
    payload = models.CharField(max_length=1, choices=(("0", "0"), ("1", "1")))
    name = models.CharField(max_length=255)
    device = models.ForeignKey(Device, related_name='buttons', on_delete=models.CASCADE)
    color = models.CharField(max_length=255, choices=(
        ("default", "White"),
        ("primary", "Blue"),
        ("success", "Green"),
        ("info", "Light blue"),
        ("warning", "Orange"),
        ("danger", "Red"),
    ), default="default")
    priority = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    manually_active = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseButton, related_name="wired", parent_link=True, on_delete=models.CASCADE)

    def perform_action_internal(self, manually=False):
        self.active = True
        self.manually_active = manually
        for b in self.device.buttons.all():
            if b.name != self.name:
                b.active = False
                b.manually_active = False
                b.save()
        self.save()
        set_state(self.device.gpio, int(self.payload))

    def perform_action(self):
        for s in self.schedule_off.all():
            s.disable_until = s.get_state()['end']
            s.save()
        for s in self.schedule_on.all():
            s.disable_until = s.get_state()['end']
            s.save()
        self.perform_action_internal(manually=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

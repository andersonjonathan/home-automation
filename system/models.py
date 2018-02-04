import os

from django.db import models

from common.models import BaseDevice, BaseButton, Room


class Device(BaseDevice):
    name = models.CharField(max_length=255, unique=True)
    room = models.ForeignKey(Room, null=True, blank=True, related_name='system', on_delete=models.CASCADE)
    hide_schedule = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseDevice, related_name="system", parent_link=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Button(BaseButton):
    name = models.CharField(max_length=255)
    call = models.CharField(max_length=1023)
    device = models.ForeignKey(Device, related_name='buttons', on_delete=models.CASCADE)
    color = models.CharField(max_length=255, choices=(
        ("default", "White"),
        ("primary", "Blue"),
        ("success", "Green"),
        ("info", "Light blue"),
        ("warning", "Orange"),
        ("danger", "Red"),
    ), default="default")
    active = models.BooleanField(default=False)
    manually_active = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseButton, related_name="system", parent_link=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{name} [{device}]'.format(name=self.name, device=self.device.name)

    def perform_action_internal(self, manually=False):
        self.active = True
        self.manually_active = manually
        for b in self.device.buttons.all():
            if b.name != self.name:
                b.active = False
                b.manually_active = False
                b.save()
        self.save()
        os.system(self.call)

    def perform_action(self):
        for s in self.schedule_off.all():
            s.disable_until = s.get_state()['end']
            s.save()
        for s in self.schedule_on.all():
            s.disable_until = s.get_state()['end']
            s.save()
        self.perform_action_internal(manually=True)

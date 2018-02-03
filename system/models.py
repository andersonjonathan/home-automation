from __future__ import unicode_literals

from subprocess import call

from django.db import models

from common.models import BaseDevice, BaseButton, Room


class Device(BaseDevice):
    name = models.CharField(max_length=255, unique=True)
    room = models.ForeignKey(Room, null=True, blank=True, related_name='system')
    parent = models.OneToOneField(BaseDevice, related_name="system", parent_link=True)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class Button(BaseButton):
    name = models.CharField(max_length=255)
    call = models.CharField(max_length=1023)
    device = models.ForeignKey(Device, related_name='buttons')
    color = models.CharField(max_length=255, choices=(
        ("default", "White"),
        ("primary", "Blue"),
        ("success", "Green"),
        ("info", "Light blue"),
        ("warning", "Orange"),
        ("danger", "Red"),
    ), default="default")

    parent = models.OneToOneField(BaseButton, related_name="system", parent_link=True)

    def __unicode__(self):
        return '{name} [{device}]'.format(name=self.name, device=self.device.name)

    def perform_action_internal(self):
        call([self.call])

    def perform_action(self):
        self.perform_action_internal()

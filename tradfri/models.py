from django.db import models

from common.models import BaseButton, BaseDevice, Room
from pytradfri import Gateway as TradfriGateway
from pytradfri.api.libcoap_api import APIFactory

import uuid


class Gateway(models.Model):
    host = models.CharField(max_length=15)
    key = models.CharField(max_length=16)
    identity = models.CharField(max_length=255)
    psk = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(Gateway, self).__init__(*args, **kwargs)
        self._initial_host = self.host
        self._initial_key = self.key

    def save(self, *args, **kwargs):
        if not self.id or self._initial_host != self.host or self._initial_key != self.key:
            self.identity = uuid.uuid4().hex
            api_factory = APIFactory(host=self.host, psk_id=self.identity)
            self.psk = api_factory.generate_psk(self.key)
        super(Gateway, self).save(*args, **kwargs)

    def __str__(self):
        return self.host

    def get_api(self):
        api_factory = APIFactory(host=self.host, psk_id=self.identity, psk=self.psk)
        return api_factory.request

    @staticmethod
    def set_dimmer(api, light, value):
        # value between 1 and 254
        if value < 1:
            value = 1
        elif value > 254:
            value = 254
        command = light.light_control.set_dimmer(value)
        api(command)
        return value

    @staticmethod
    def get_dimmer(light):
        return light.light_control.lights[0].dimmer

    @staticmethod
    def get_color_temp(light):
        return light.light_control.lights[0].color_temp

    @staticmethod
    def set_color(api, light, value):
        # value between 250 and 454
        if value < 250:
            value = 250
        elif value > 454:
            value = 454
        command = light.light_control.set_color_temp(value)
        api(command)
        return value

    @staticmethod
    def set_state(api, light, on):
        if on >= 1:
            on = True
        else:
            on = False
        command = light.light_control.set_state(on)
        api(command)
        return on

    @staticmethod
    def get_lights(api):
        gateway = TradfriGateway()
        devices_command = gateway.get_devices()
        devices_commands = api(devices_command)
        devices = api(devices_commands)
        return [dev for dev in devices if dev.has_light_control]

    @staticmethod
    def get_light(api, device_id):
        gateway = TradfriGateway()
        device_command = gateway.get_device(device_id)
        device = api(device_command)
        return device


class TradfriLight(models.Model):
    gateway = models.ForeignKey(Gateway, related_name='lights', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    light_id = models.IntegerField()

    class Meta:
        unique_together = (('gateway', 'light_id'),)

    def __str__(self):
        return self.name


class Device(BaseDevice):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, null=True, blank=True, related_name='tradfri', on_delete=models.CASCADE)
    hide_schedule = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseDevice, related_name="tradfri", parent_link=True, on_delete=models.CASCADE)
    state = models.IntegerField(default=1)
    dimmer = models.IntegerField(default=1)
    color = models.IntegerField(default=250)
    def __str__(self):
        return '{name}{room}'.format(name=self.name, room=', ' + self.room.name if self.room else '')


class Button(BaseButton):
    name = models.CharField(max_length=255)
    gateway = models.ForeignKey(Gateway, related_name='buttons', on_delete=models.CASCADE)
    lights = models.ManyToManyField(TradfriLight)
    function = models.CharField(max_length=255, choices=(
        ("set_state", "state"),
        ("set_dimmer", "dimmer"),
        ("set_color", "color"),
    ), default="state", help_text="Allowed values state=[0:1], dimmer=[1:254], color=[250:454]")
    action_value = models.IntegerField(default=1)
    action = models.CharField(max_length=255, choices=(
        ("add", "add"),
        ("subtract", "subtract"),
        ("fixed", "fixed"),
    ), default="state")
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
    parent = models.OneToOneField(BaseButton, related_name="tradfri", parent_link=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'device'),)
        ordering = ["priority"]

    def __str__(self):
        return '{name} [{device}]'.format(name=self.name, device=self.device.name)

    def perform_action_internal(self, manually=False):
        if self.function == 'set_state':
            self.active = True
            self.manually_active = manually
            for b in self.device.buttons.all():
                if b.name != self.name:
                    b.active = False
                    b.manually_active = False
                    b.save()
            self.save()
        api = self.gateway.get_api()
        new_value = 0
        if self.function == 'set_state':
            new_value = self.device.state
        elif self.function == 'set_dimmer':
            new_value = self.device.dimmer
        elif self.function == 'set_color':
            new_value = self.device.color

        if self.action == 'add':
            new_value += self.action_value
        elif self.action == 'subtract':
            new_value -= self.action_value
        elif self.action == 'fixed':
            new_value = self.action_value

        for db_light in self.lights.all():
            light = self.gateway.get_light(api, db_light.light_id)
            if self.function == 'set_state':
                self.device.state = self.gateway.set_state(api, light, new_value)
            elif self.function == 'set_dimmer':
                self.device.dimmer = self.gateway.set_dimmer(api, light, new_value)
            elif self.function == 'set_color':
                self.device.color = self.gateway.set_color(api, light, new_value)
        self.device.save()

    def perform_action(self):
        for s in self.schedule_off.all():
            s.disable_until = s.get_state()['end']
            s.save()
        for s in self.schedule_on.all():
            s.disable_until = s.get_state()['end']
            s.save()
        self.perform_action_internal(manually=True)



from django.db import models

from common.exceptions import UnknownCommand
from common.models import BaseButton, BaseDevice, Room
from radio.utils import transmit


class RadioTransmitter(models.Model):
    name = models.CharField(max_length=255)
    gpio = models.CharField(max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.name)


class RadioProtocol(models.Model):
    name = models.CharField(max_length=255)
    time = models.FloatField(help_text="Period time t in seconds")

    def __str__(self):
        return '{name}'.format(name=self.name)


class RadioSignal(models.Model):
    protocol = models.ForeignKey(RadioProtocol, on_delete=models.CASCADE)
    char = models.CharField(max_length=1)
    on = models.IntegerField(help_text="Nr of periods on")
    off = models.IntegerField(help_text="Nr of periods off")

    class Meta:
        unique_together = (('protocol', 'char'),)

    def __str__(self):
        return '{protocol} [{char}] [ON: {on}, OFF: {off}]'.format(
            protocol=self.protocol, char=self.char, on=self.on, off=self.off)


class RadioCode(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    payload = models.CharField(max_length=255)
    transmitter = models.ForeignKey(RadioTransmitter, blank=False, null=True, on_delete=models.CASCADE)
    protocol = models.ForeignKey(RadioProtocol, on_delete=models.CASCADE)
    
    def signals(self):
        return list(self.protocol.radiosignal_set.all())
    
    def time(self):
        return self.protocol.time

    def __str__(self):
        return '{protocol} - {name} [{transmitter}]'.format(
            protocol=self.protocol, name=self.name, transmitter=self.transmitter)


class Device(BaseDevice):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, null=True, blank=True, related_name='radio', on_delete=models.CASCADE)
    hide_schedule = models.BooleanField(default=False)
    parent = models.OneToOneField(BaseDevice, related_name="radio", parent_link=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{name}{room}'.format(name=self.name, room=', ' + self.room.name if self.room else '')


class Button(BaseButton):
    name = models.CharField(max_length=255)
    radio_code = models.ForeignKey(RadioCode, related_name='buttons', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, related_name='buttons', on_delete=models.CASCADE)
    rounds = models.IntegerField(default=10)
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
    parent = models.OneToOneField(BaseButton, related_name="radio", parent_link=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'device'),)
        ordering = ["priority"]

    def __str__(self):
        return '{name} [{device}]'.format(name=self.name, device=self.device.name)

    def _format_payload(self, str_payload):
        str_payload = str_payload.replace(" ", "")
        signals = self.radio_code.signals()
        t = self.radio_code.time()
        payload = []
        for c in str_payload:
            on = None
            off = None
            for s in signals:
                if s.char.lower() == c.lower():
                    on = s.on
                    off = s.off
                    break

            if on is not None:
                payload.append((1, on*t))
            else:
                raise UnknownCommand()

            if off is not None:
                payload.append((0, off*t))
            else:
                raise UnknownCommand()
        return payload

    def perform_action_internal(self, manually=False):
        self.active = True
        self.manually_active = manually
        for b in self.device.buttons.all():
            if b.name != self.name:
                b.active = False
                b.manually_active = False
                b.save()
        self.save()
        payload = self._format_payload(self.radio_code.payload)
        transmit(payload, self.radio_code.transmitter.gpio, self.rounds)

    def perform_action(self):
        for s in self.schedule_off.all():
            s.disable_until = s.get_state()['end']
            s.save()
        for s in self.schedule_on.all():
            s.disable_until = s.get_state()['end']
            s.save()
        self.perform_action_internal(manually=True)

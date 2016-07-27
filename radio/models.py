from __future__ import unicode_literals

from django.db import models

from common.exceptions import UnknownCommand
from common.models import BaseButton, BaseDevice
from radio.utils import transmit


class RadioTransmitter(models.Model):
    name = models.CharField(max_length=255)
    gpio = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class RadioProtocol(models.Model):
    name = models.CharField(max_length=255)
    time = models.FloatField(help_text="Period time t in seconds")

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class RadioSignal(models.Model):
    protocol = models.ForeignKey(RadioProtocol)
    char = models.CharField(max_length=1)
    on = models.IntegerField(help_text="Nr of periods on")
    off = models.IntegerField(help_text="Nr of periods off")

    class Meta:
        unique_together = (('protocol', 'char'),)

    def __unicode__(self):
        return u'{protocol} [{char}] [ON: {on}, OFF: {off}]'.format(
            protocol=self.protocol, char=self.char, on=self.on, off=self.off)


class RadioCode(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    payload = models.CharField(max_length=255)
    transmitter = models.ForeignKey(RadioTransmitter, blank=False, null=True)
    protocol = models.ForeignKey(RadioProtocol)
    
    def signals(self):
        return list(self.protocol.radiosignal_set.all())
    
    def time(self):
        return self.protocol.time


class Device(BaseDevice):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class Button(BaseButton):
    name = models.CharField(max_length=255)
    radio_code = models.ForeignKey(RadioCode, related_name='buttons')
    device = models.ForeignKey(Device, related_name='buttons')
    rounds = models.IntegerField(default=10)
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

    class Meta:
        unique_together = (('name', 'device'),)
        ordering = ["priority"]

    def __unicode__(self):
        return u'{name} [{device}]'.format(name=self.name, device=self.device.name)

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

    def perform_action_internal(self):
        payload = self._format_payload(self.radio_code.payload)
        transmit(payload, self.radio_code.transmitter.gpio, self.rounds)

    def perform_action(self):
        self.active = True
        for b in self.device.buttons.all():
            if b.name != self.name:
                b.active = False
                b.save()
        self.save()
        self.perform_action_internal()

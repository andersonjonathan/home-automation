from __future__ import unicode_literals

from django.db import models


class BaseDevice(models.Model):
    def child(self):
        if hasattr(self, 'radioplug'):
            return self.radioplug
        if hasattr(self, 'wiredplug'):
            return self.wiredplug
        if hasattr(self, 'irdevice'):
            return self.irdevice
        if hasattr(self, 'kodidevice'):
            return self.kodidevice


class BaseButton(models.Model):
    def perform_action_internal(self):
        raise NotImplementedError("Please Implement this method")

    def perform_action(self):
        raise NotImplementedError("Please Implement this method")


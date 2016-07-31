from __future__ import unicode_literals

from django.db import models


class BaseDevice(models.Model):
    @property
    def child(self):
        if hasattr(self, 'radio'):
            return self.radio
        if hasattr(self, 'wired'):
            return self.wired
        if hasattr(self, 'infrared'):
            return self.infrared
        if hasattr(self, 'kodi'):
            return self.kodi

    def has_auto(self):
        pass

    def __unicode__(self):
        return self.child.__unicode__()


class BaseButton(models.Model):
    @property
    def child(self):
        if hasattr(self, 'radio'):
            return self.radio
        if hasattr(self, 'wired'):
            return self.wired
        if hasattr(self, 'infrared'):
            return self.infrared
        if hasattr(self, 'kodi'):
            return self.kodi

    def __unicode__(self):
        return self.child.__unicode__()

    def perform_action_internal(self):
        raise NotImplementedError("Please Implement this method")

    def perform_action(self):
        raise NotImplementedError("Please Implement this method")


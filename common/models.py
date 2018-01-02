from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('room', args=[self.name])


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
        if hasattr(self, 'api'):
            return self.api

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
        if hasattr(self, 'api'):
            return self.api

    def __unicode__(self):
        return self.child.__unicode__()

    def perform_action_internal(self):
        raise NotImplementedError("Please Implement this method")

    def perform_action(self):
        raise NotImplementedError("Please Implement this method")


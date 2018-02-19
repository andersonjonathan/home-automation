from django.db import models
from django.urls import reverse


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
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
        if hasattr(self, 'system'):
            return self.system
        if hasattr(self, 'tradfri'):
            return self.tradfri

    def has_auto(self):
        pass

    def __str__(self):
        return self.child.__str__()


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
        if hasattr(self, 'system'):
            return self.system
        if hasattr(self, 'tradfri'):
            return self.tradfri

    def __str__(self):
        return self.child.__str__()

    def perform_action_internal(self):
        raise NotImplementedError("Please Implement this method")

    def perform_action(self):
        raise NotImplementedError("Please Implement this method")


class Url(models.Model):
    url = models.TextField()
    name = models.TextField()

    def __str__(self):
        return self.name

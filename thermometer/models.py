from __future__ import unicode_literals

from django.db import models
from utils import read_retry, read_capacitor, w1_read_temp


class DHT11(models.Model):
    name = models.CharField(max_length=254)
    gpio = models.IntegerField(help_text="GPIO port", unique=True)

    @property
    def temperature(self):
        return self.read_retry[1]

    @property
    def humidity(self):
        return self.read_retry[0]

    @property
    def read_retry(self):
        return read_retry(self.gpio)

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class CapacitorDevice(models.Model):
    name = models.CharField(max_length=254)
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    a = models.FloatField(help_text="y=a*ln(x)+b")
    b = models.FloatField(help_text="y=a*ln(x)+b")
    unit = models.CharField(max_length=254, null=True, blank=True)

    @property
    def value(self):
        return read_capacitor(self.gpio, self.a, self.b)

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class W1Therm(models.Model):
    name = models.CharField(max_length=254)
    unit = models.CharField(max_length=254, null=True, blank=True)

    @property
    def temperature(self):
        return w1_read_temp()

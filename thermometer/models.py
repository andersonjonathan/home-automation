from __future__ import unicode_literals

from django.db import models
from utils import read_retry


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

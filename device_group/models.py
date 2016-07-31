from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from common.models import BaseDevice


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    devices = models.ManyToManyField(BaseDevice, through='GroupDeviceRelation')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', args=[self.name])


class GroupDeviceRelation(models.Model):
    device = models.ForeignKey(BaseDevice)
    group = models.ForeignKey(Group)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

from __future__ import unicode_literals

from subprocess import call

from django.db import models

from common.models import BaseDevice, BaseButton


class Config(models.Model):
    name = models.CharField(max_length=255)
    remote = models.CharField(max_length=255)
    key = models.CharField(max_length=255)


class Device(BaseDevice):
    name = models.CharField(max_length=255, unique=True)
    parent = models.OneToOneField(BaseDevice, related_name="infrared", parent_link=True)

    def button_grid(self):
        btns = self.buttons.all().order_by('row', 'priority')
        if not btns:
            return btns
        res = []
        row = []
        prev_row = btns[0].row
        for b in btns:
            if prev_row == b.row:
                row.append(b)
            else:
                res.append(row)
                row = []
                prev_row = b.row

        return res


class Button(BaseButton):
    name = models.CharField(max_length=255)
    config = models.ForeignKey(Config, related_name='buttons')
    device = models.ForeignKey(Device, related_name='buttons')
    count = models.IntegerField(default=10)
    color = models.CharField(max_length=255, choices=(
        ("btn-default", "White"),
        ("btn-primary", "Blue"),
        ("btn-success", "Green"),
        ("btn-info", "Light blue"),
        ("btn-warning", "Orange"),
        ("btn-danger", "Red"),
    ), default="btn-default")
    row = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    parent = models.OneToOneField(BaseButton, related_name="infrared", parent_link=True)

    def __unicode__(self):
        return u'{name} [{plug}]'.format(name=self.name, plug=self.plug.name)

    def perform_action_internal(self):
        call(['irsend', 'SEND_ONCE', self.remote, self.key, "--count={}".format(self.count)])

    def perform_action(self):
        self.perform_action_internal()

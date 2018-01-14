from __future__ import unicode_literals

import requests
from django.db import models

from common.models import BaseDevice, BaseButton, Room


class Device(BaseDevice):
    name = models.CharField(max_length=255, unique=True)
    room = models.ForeignKey(Room, null=True, blank=True, related_name='api')
    parent = models.OneToOneField(BaseDevice, related_name="api", parent_link=True)

    def __unicode__(self):
        return '{name}{room}'.format(name=self.name, room=', ' + self.room.name if self.room else '')


class Button(BaseButton):
    device = models.ForeignKey(Device, related_name='buttons')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, choices=(
        ("default", "White"),
        ("primary", "Blue"),
        ("success", "Green"),
        ("info", "Light blue"),
        ("warning", "Orange"),
        ("danger", "Red"),
    ), default="btn-default")
    url = models.CharField(max_length=511)
    post_body = models.TextField(blank=True, null=True)
    content_type = models.CharField(default="application/json", max_length=255, blank=True, null=True)
    method = models.CharField(max_length=10, choices=(
        ("post", "POST"),
        ("get", "GET"),))
    user = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    parent = models.OneToOneField(BaseButton, related_name="api", parent_link=True)
    active = models.BooleanField(default=False)
    manually_active = models.BooleanField(default=False)

    class Meta:
        unique_together = (('name', 'device'),)

    def __unicode__(self):
        return '{name}'.format(name=self.name)

    def perform_action_internal(self, manually=False):
        self.active = True
        self.manually_active = manually
        for b in self.device.buttons.all():
            if b.pk != self.pk:
                b.active = False
                b.manually_active = False
                b.save()
        self.save()
        if self.method == 'post':
            auth = None
            headers = {
                'cache-control': "no-cache",
            }
            if self.user:
                auth = (self.user, self.password)
            if self.content_type:
                headers['content-type'] = self.content_type
            requests.post(
                self.url,
                data=self.post_body,
                headers=headers,
                auth=auth
            )
        elif self.method == 'get':
            auth = None
            if self.user:
                auth = (self.user, self.password)
            requests.get(
                self.url,
                headers={
                    'cache-control': "no-cache",
                },
                auth=auth
            )

    def perform_action(self):
        for s in self.schedule_off.all():
            s.disable_until = s.get_state()['end']
            s.save()
        for s in self.schedule_on.all():
            s.disable_until = s.get_state()['end']
            s.save()
        self.perform_action_internal(manually=True)

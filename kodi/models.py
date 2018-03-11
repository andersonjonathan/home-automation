import requests
from django.db import models

from common.models import BaseDevice, BaseButton


class Device(BaseDevice):
    name = models.CharField(max_length=255, unique=True)
    host = models.CharField(max_length=16)
    port = models.CharField(max_length=16)
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    parent = models.OneToOneField(BaseDevice, related_name="kodi", parent_link=True, on_delete=models.CASCADE)

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
                row = [b]
                prev_row = b.row
        res.append(row)
        return res

    def __str__(self):
        return '{name}'.format(name=self.name)


class Button(BaseButton):
    device = models.ForeignKey(Device, related_name='buttons', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
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
    parent = models.OneToOneField(BaseButton, related_name="kodi", parent_link=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'device'),)
        ordering = ["row", "priority"]

    def __str__(self):
        return '{name} [{kodi}]'.format(name=self.name, kodi=self.device.name)

    def perform_action_internal(self, *args, **kwargs):
        url = "http://{host}:{port}/jsonrpc".format(host=self.device.child.host, port=self.device.child.port)
        payload = "{{\"jsonrpc\": \"2.0\", \"id\": 1, \"method\": \"{method}\"}}".format(method=self.method)
        headers = {
            'cache-control': "no-cache",
        }
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=(self.device.child.user, self.device.child.password)
        )
        return response.text

    def perform_action(self, *args, **kwargs):
        self.perform_action_internal(*args, **kwargs)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Group


@login_required
def group(request, group_name):
    context = {'current_page': group_name,
               'devices': Group.objects.get(name=group_name).devices.all(),
               'plugs': [str('radio_device'), str('wired_device')]}
    return render(request, 'device_group/index.html', context)

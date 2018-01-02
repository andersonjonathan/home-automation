from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from common.models import BaseDevice


@login_required
def buttons(request, device_pk):
    device = BaseDevice.objects.get(pk=device_pk).child
    btns = []
    for b in device.buttons.all():
        btns.append({
            'optionValue': b.pk,
            'optionDisplay': unicode(b)
        })
    return JsonResponse({'status': 'ok', 'buttons': btns})

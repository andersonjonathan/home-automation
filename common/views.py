from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import FieldError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters

from common.models import BaseDevice
from infrared.models import Device as IRDevice
from kodi.models import Device as KodiDevice
from radio.models import Device as RadioDevice
from schedules.models import Schedule
from wired.models import Device as WiredDevice

from django.http import JsonResponse


@login_required
def index(request):
    context = {'current_page': 'Devices',
               'remotes': list(IRDevice.objects.all()) + list(KodiDevice.objects.all()),
               'plugs': list(RadioDevice.objects.all()) + list(WiredDevice.objects.all())}
    return render(request, 'common/index.html', context)


@login_required
def switch(request, pk, button_pk):
    device = BaseDevice.objects.get(pk=pk).child
    if button_pk == "auto":
        try:
            for btn in device.buttons.filter(active=True):
                btn.active = False
                btn.save()
        except (FieldError, AttributeError):
            pass

        schedules = device.schedule_set.filter(active=False)
        for schedule in schedules:
            schedule.active = True
            schedule.save()
        return JsonResponse({"status": "ok"})
    try:
        btn = device.buttons.get(pk=button_pk).child
        btn.perform_action()
        schedules = device.schedule_set.filter(active=True)
        for schedule in schedules:
            schedule.active = False
            schedule.save()
        try:
            for b in device.buttons.filter(active=True):
                b.active = False
                b.save()
            btn.active = True
            btn.save()
        except (FieldError, AttributeError):
            pass

    except KeyError:
        return JsonResponse({"status": "Exception."})
    return JsonResponse({"status": "ok"})


@sensitive_post_parameters()
@csrf_exempt
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
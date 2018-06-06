from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters

from common.models import BaseDevice
from api.models import Device as ApiDevice
from infrared.models import Device as IRDevice
from kodi.models import Device as KodiDevice
from radio.models import Device as RadioDevice
from system.models import Device as SystemDevice
from wired.models import Device as WiredDevice
from tradfri.models import Device as TradfriDevice

from django.http import JsonResponse, HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView

@login_required
def index(request):
    plugs = sorted(list(RadioDevice.objects.all()) + list(WiredDevice.objects.all()) +
                   list(ApiDevice.objects.all()) + list(SystemDevice.objects.all()) + list(TradfriDevice.objects.all()),
                   key=lambda x: (x.room is None, x.room.name if x.room else None))
    context = {'current_page': 'Devices',
               'remotes': list(IRDevice.objects.all()) + list(KodiDevice.objects.all()),
               'plugs': plugs}

    return render(request, 'common/index.html', context)


@login_required
def room(request, room_name):
    context = {'current_page': room_name,
               'remotes': [],
               'plugs': list(RadioDevice.objects.filter(room__name=room_name)) +
                        list(WiredDevice.objects.filter(room__name=room_name)) +
                        list(ApiDevice.objects.filter(room__name=room_name)) +
                        list(SystemDevice.objects.filter(room__name=room_name)) +
                        list(TradfriDevice.objects.filter(room__name=room_name))}
    return render(request, 'common/index.html', context)


@login_required
def switch(request, pk, button_pk):
    device = BaseDevice.objects.get(pk=pk).child
    try:
        btn = device.buttons.get(pk=button_pk).child
        btn.perform_action()

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


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')
from django import template

from ..models import DHT11, CapacitorDevice, W1Therm, MCP3008Channel

register = template.Library()


@register.assignment_tag()
def get_thermometers():
    return DHT11.objects.all()


@register.assignment_tag()
def get_capacitor_devices():
    return CapacitorDevice.objects.all()


@register.assignment_tag()
def get_w1_devices():
    return W1Therm.objects.all()


@register.assignment_tag()
def get_mcp3008_devices():
    return MCP3008Channel.objects.all()

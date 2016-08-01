from django import template

from ..models import DHT11, CapacitorDevice

register = template.Library()


@register.assignment_tag()
def get_thermometers():
    return DHT11.objects.all()


@register.simple_tag()
def get_temperature(instance):
    """
    Returns verbose_name for a field.
    """
    return instance.temperature


@register.simple_tag()
def get_humidity(instance):
    """
    Returns verbose_name for a field.
    """
    return instance.humidity


@register.assignment_tag()
def get_capacitor_devices():
    return CapacitorDevice.objects.all()


@register.simple_tag()
def get_capacitor_device_value(instance):
    """
    Returns verbose_name for a field.
    """
    return instance.temperature

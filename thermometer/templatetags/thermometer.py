from django import template

from ..models import DHT11, CapacitorDevice, W1Therm

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
    return instance.value


@register.simple_tag()
def get_capacitor_device_value_int(instance):
    """
    Returns verbose_name for a field.
    """
    return int(instance.value)


@register.assignment_tag()
def get_w1_devices():
    return W1Therm.objects.all()

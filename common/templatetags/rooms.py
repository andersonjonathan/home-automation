from django import template

from ..models import Room, Url

register = template.Library()


@register.assignment_tag()
def get_rooms():
    """
    Returns verbose_name for a field.
    """
    return Room.objects.all()

@register.assignment_tag()
def get_urls():
    """
    Returns verbose_name for a field.
    """
    return Url.objects.all()

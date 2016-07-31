from django import template

from ..models import Group

register = template.Library()


@register.assignment_tag()
def get_groups():
    """
    Returns verbose_name for a field.
    """
    return Group.objects.all()

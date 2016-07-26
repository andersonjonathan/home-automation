from django import template
register = template.Library()

@register.assignment_tag()
def get_verbose_field_name(instance):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.verbose_name.title()
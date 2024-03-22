from django import template

register = template.Library()

@register.filter
def remove_decimal_if_integer(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value
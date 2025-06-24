from django import template
import math

register = template.Library()

# Custom template tag to perform arithmetical ops
@register.filter(name='divide_by')
def divide_by(value, arg):
    """Divides the value by the argument."""
    try:
        return math.floor(value / arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter(name='split')
def split(value, delimiter=','):
    return value.split(delimiter)

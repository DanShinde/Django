
# gallery/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(string, suffix):
    return string.endswith(suffix)

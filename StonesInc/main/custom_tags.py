from django import template
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def my_static(path):
    return static(path)

@register.simple_tag
def my_script(path):
    return static(path)

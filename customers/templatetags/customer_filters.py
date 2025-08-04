from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

@register.filter
def starts_with_http(value):
    """Verifica se a string começa com 'http'"""
    if value:
        return value.startswith('http')
    return False 
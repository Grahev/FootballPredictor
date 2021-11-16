from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter()
def MD(value):
    return value.matchday.split("-")[-1]
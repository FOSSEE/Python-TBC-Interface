from django import template
from django.conf import settings

register = template.Library()

@register.filter
def lookup(List, i):
    try:
        return List[i-1]
    except IndexError:
        return "Chapter " + str(i) + " name" 

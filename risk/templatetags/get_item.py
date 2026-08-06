# create folder risk/templatetags/__init__.py (empty)
# then this file:
from django import template
register = template.Library()

@register.filter
def get_item(d, k):
    return d.get(k, '')

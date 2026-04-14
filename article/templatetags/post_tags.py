from django import template
from django.utils.safestring import mark_safe

from markdown import markdown

register = template.Library()

@register.filter(name="post_markdown")
def post_markdown(value):
    return mark_safe(markdown(value))
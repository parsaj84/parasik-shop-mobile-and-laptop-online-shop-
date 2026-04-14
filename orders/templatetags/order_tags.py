from django.template import Library

import json

register = Library()

@register.filter(name="json_loader")
def json_loader(json_):
    return json.loads(json_)
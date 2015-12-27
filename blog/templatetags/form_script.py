from django import template
from django.template import Context
from django.template.loader import render_to_string

import re

register = template.Library()

@register.inclusion_tag('tag-form-script.html')
def form_script():
    return {}

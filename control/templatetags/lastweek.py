from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta

register = template.Library()

@register.simple_tag
def lastweek(format_string):
    return (datetime.now()+timedelta(weeks=-1)).strftime(format_string)
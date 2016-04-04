from django.utils import timezone
from django import template

register = template.Library()

@register.filter
def expired(time):
    current_time = timezone.now()
    return time < current_time

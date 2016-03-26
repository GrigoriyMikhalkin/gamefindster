from django.utils import six
from django.utils.functional import allow_lazy

def get_object_or_none(model,*args,**kwargs):
    try:
        obj = model.objects.get(*args,**kwargs)
    except model.DoesNotExist:
        return None
    
    return obj

def format_lazy(string, *args, **kwargs):
    return string.format(*args, **kwargs)

format_lazy = allow_lazy(format_lazy,six.text_type)

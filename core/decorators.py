from django.core.exceptions import PermissionDenied
from Employement.models import Manager

def manager_required(function):
    def wrap(request, *args, **kwargs):
        if Manager.objects.filter(pk=kwargs['pk']).exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

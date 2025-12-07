# permissions.py
from rolepermissions.checkers import has_permission
from django.http import HttpResponseForbidden
from functools import wraps

def role_permission_required(permission_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            
            if has_permission(request.user, permission_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission.")
        return wrapper
    return decorator
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator for views that checks if the logged-in user has one of the allowed roles.
    If the user is not authenticated, redirect to login.
    If the user does not have the required role, raise PermissionDenied.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('getskills:login')
            
            # Admins always have access to everything
            if request.user.role == 'ADMIN':
                return view_func(request, *args, **kwargs)
                
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
                
            raise PermissionDenied("Anda tidak memiliki akses ke halaman ini.")
        return _wrapped_view
    return decorator

from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def superuser_required(view_func):
    """
    Decorator for views that checks whether the logged-in user is a Super User.
    Enforces strict server-side role-based permission system.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Access denied. Please log in with a Super User account.")
            return redirect(f"/login/?next={request.path}")
        
        if not request.user.is_superuser:
            # Raise PermissionDenied which triggers HTTP 403 Forbidden
            messages.error(request, "403 Forbidden: You do not have permission to access administrative management features.")
            raise PermissionDenied("Only Super Users can access management features.")
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

class SuperUserRequiredMixin:
    """
    CBV mixin that verifies the current user is an authenticated Super User.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Access denied. Please log in with a Super User account.")
            return redirect(f"/login/?next={request.path}")
            
        if not request.user.is_superuser:
            messages.error(request, "403 Forbidden: You do not have permission to access administrative management features.")
            raise PermissionDenied("Only Super Users can access management features.")
            
        return super().dispatch(request, *args, **kwargs)

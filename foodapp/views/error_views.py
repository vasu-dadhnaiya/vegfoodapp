from django.shortcuts import render

def custom_permission_denied(request, exception=None):
    """Custom HTTP 403 Forbidden Access Denied handler."""
    return render(request, '403.html', {
        'exception': str(exception) if exception else "You do not have permission to perform this management action."
    }, status=403)

def custom_page_not_found(request, exception=None):
    """Custom HTTP 404 Page Not Found handler."""
    return render(request, '404.html', status=404)

def custom_server_error(request):
    """Custom HTTP 500 Server Error handler."""
    return render(request, '500.html', status=500)

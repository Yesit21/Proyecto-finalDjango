"""
Custom middleware for Railway deployment
"""


class HealthCheckMiddleware:
    """
    Middleware to bypass ALLOWED_HOSTS validation for healthcheck endpoint
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow healthcheck endpoint without ALLOWED_HOSTS validation
        if request.path == '/health/':
            # Temporarily add the host to ALLOWED_HOSTS for this request
            from django.conf import settings
            original_allowed_hosts = settings.ALLOWED_HOSTS
            if request.get_host() not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + [request.get_host()]
            
            response = self.get_response(request)
            
            # Restore original ALLOWED_HOSTS
            settings.ALLOWED_HOSTS = original_allowed_hosts
            return response
        
        return self.get_response(request)

"""
Healthcheck view for Railway deployment
This view bypasses ALLOWED_HOSTS validation
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def healthcheck(request):
    """
    Simple healthcheck endpoint for Railway
    Returns 200 OK if the application is running
    """
    return JsonResponse({
        "status": "healthy",
        "service": "restaurante_project"
    }, status=200)

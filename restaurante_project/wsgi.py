"""
WSGI config for restaurante_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Forzar el uso del archivo de settings correcto
os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurante_project.settings'

print(f"Cargando WSGI con SETTINGS: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI application cargada exitosamente.")
except Exception as e:
    print(f"ERROR CRITICO AL CARGAR WSGI: {e}")
    raise e

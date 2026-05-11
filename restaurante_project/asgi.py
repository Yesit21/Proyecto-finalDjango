<<<<<<< HEAD
"""
ASGI config for restaurante_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante_project.settings')

=======
﻿import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
>>>>>>> 39418a775c31a7f8bd147b2090d267aec03ff655
application = get_asgi_application()

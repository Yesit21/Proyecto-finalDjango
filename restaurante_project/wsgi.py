<<<<<<< HEAD
"""
WSGI config for restaurante_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante_project.settings')

=======
﻿import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
>>>>>>> 39418a775c31a7f8bd147b2090d267aec03ff655
application = get_wsgi_application()

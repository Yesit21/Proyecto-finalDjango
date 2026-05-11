<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/usuarios/login/', permanent=False)),
    path('usuarios/', include('apps.usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
﻿from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('menu/', include('apps.menu.urls')),
    path('reservas/', include('apps.reservas.urls')),
    path('reportes-api/', include('apps.reportes.urls')),
]
>>>>>>> 39418a775c31a7f8bd147b2090d267aec03ff655

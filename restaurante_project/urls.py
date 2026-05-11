from django.contrib import admin
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

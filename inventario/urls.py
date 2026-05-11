from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario_lista, name='lista'),
    path('movimiento/crear/', views.movimiento_crear, name='movimiento_crear'),
    path('movimientos/', views.movimientos_lista, name='movimientos'),
    path('proveedores/', views.proveedores_lista, name='proveedores'),
    path('proveedor/crear/', views.proveedor_crear, name='proveedor_crear'),
    path('ordenes/', views.ordenes_compra_lista, name='ordenes'),
]

from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('movimientos/', views.historial_movimientos, name='historial'),
    path('movimiento/crear/', views.crear_movimiento, name='crear_movimiento'),
]

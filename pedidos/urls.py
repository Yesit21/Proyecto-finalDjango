from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/agregar/<int:plato_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('crear/', views.crear_pedido, name='crear'),
    path('<int:pk>/', views.pedido_detalle, name='detalle'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('lista/', views.pedidos_lista, name='lista'),
    path('<int:pk>/actualizar-estado/', views.actualizar_estado_pedido, name='actualizar_estado'),
]

from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('pago/', views.pago_simulado, name='pago'),
    path('checkout/', views.realizar_pedido, name='realizar_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle'),
    path('<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar'),
    path('<int:pedido_id>/estado/', views.actualizar_estado, name='actualizar_estado'),
]

from django.contrib import admin
from .models import Pedido, PedidoItem


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado',)
    search_fields = ('cliente__username',)


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'nombre', 'cantidad', 'precio_unitario', 'subtotal')

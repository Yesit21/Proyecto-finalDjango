from django.contrib import admin
from .models import Pedido, DetallePedido, Carrito, ItemCarrito

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_pedido', 'estado', 'tipo', 'total', 'pagado']
    list_filter = ['estado', 'tipo', 'pagado', 'fecha_pedido']
    search_fields = ['cliente__username', 'id']
    inlines = [DetallePedidoInline]
    readonly_fields = ['fecha_pedido', 'total']

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [ItemCarritoInline]

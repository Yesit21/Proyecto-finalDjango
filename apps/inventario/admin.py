from django.contrib import admin
from .models import MovimientoInventario, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock_actual', 'alerta_stock')
    search_fields = ('nombre',)


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha')
    list_filter = ('tipo',)

from django.contrib import admin
from .models import MovimientoInventario, Proveedor, OrdenCompra, DetalleOrdenCompra

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['ingrediente', 'tipo', 'cantidad', 'fecha', 'usuario']
    list_filter = ['tipo', 'fecha']
    search_fields = ['ingrediente__nombre', 'motivo']
    date_hierarchy = 'fecha'

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto', 'telefono', 'email', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'contacto']

class DetalleOrdenCompraInline(admin.TabularInline):
    model = DetalleOrdenCompra
    extra = 1

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha_orden', 'fecha_entrega_estimada', 'estado', 'total']
    list_filter = ['estado', 'fecha_orden']
    search_fields = ['proveedor__nombre']
    inlines = [DetalleOrdenCompraInline]
    date_hierarchy = 'fecha_orden'

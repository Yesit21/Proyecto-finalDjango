from django.contrib import admin
from .models import Plato, Ingrediente, PlatoIngrediente
from .forms import PlatoForm, IngredienteForm


class PlatoIngredienteInline(admin.TabularInline):
    model = PlatoIngrediente
    extra = 1
    fields = ['ingrediente', 'cantidad']


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    form = IngredienteForm
    list_display = ['nombre', 'unidad_medida', 'stock_actual', 'stock_minimo', 'precio_unitario', 'activo', 'stock_bajo']
    list_filter = ['unidad_medida', 'activo']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'unidad_medida')
        }),
        ('Stock', {
            'fields': ('stock_actual', 'stock_minimo')
        }),
        ('Precio', {
            'fields': ('precio_unitario',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    def stock_bajo(self, obj):
        return obj.stock_bajo
    stock_bajo.boolean = True
    stock_bajo.short_description = 'Stock Bajo'


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    form = PlatoForm
    list_display = ['nombre', 'categoria', 'precio', 'disponible']
    list_filter = ['categoria', 'disponible']
    search_fields = ['nombre', 'descripcion']
    ordering = ['categoria', 'nombre']
    inlines = [PlatoIngredienteInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Precio y Disponibilidad', {
            'fields': ('precio', 'disponible'),
            'description': 'El precio puede ser en cualquier moneda. Ingrese solo el valor numérico.'
        }),
        ('Imagen', {
            'fields': ('imagen',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PlatoIngrediente)
class PlatoIngredienteAdmin(admin.ModelAdmin):
    list_display = ['plato', 'ingrediente', 'cantidad', 'get_unidad']
    list_filter = ['plato__categoria']
    search_fields = ['plato__nombre', 'ingrediente__nombre']
    
    def get_unidad(self, obj):
        return obj.ingrediente.unidad_medida
    get_unidad.short_description = 'Unidad'

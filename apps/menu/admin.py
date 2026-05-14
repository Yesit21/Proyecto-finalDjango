from django.contrib import admin
from .models import Plato

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'disponible']
    list_filter = ['categoria', 'disponible']
    search_fields = ['nombre', 'descripcion']
    ordering = ['categoria', 'nombre']

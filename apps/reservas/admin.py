from django.contrib import admin
from .models import Reserva, Mesa

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidad', 'estado', 'ubicacion', 'activa']
    list_filter = ['estado', 'activa', 'ubicacion']
    search_fields = ['numero', 'ubicacion']
    ordering = ['numero']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'mesa', 'fecha_reserva', 'cantidad_personas', 'estado', 'created_at']
    list_filter = ['estado', 'fecha_reserva']
    search_fields = ['usuario__nombre', 'usuario__email', 'mesa__numero']
    ordering = ['-fecha_reserva']
    readonly_fields = ['created_at', 'updated_at']


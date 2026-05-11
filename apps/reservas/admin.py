from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_reserva', 'cantidad_personas', 'estado', 'created_at']
    list_filter = ['estado', 'fecha_reserva']
    search_fields = ['usuario__nombre', 'usuario__email']
    ordering = ['-fecha_reserva']
    readonly_fields = ['created_at', 'updated_at']


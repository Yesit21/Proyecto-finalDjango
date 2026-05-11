from django.contrib import admin
from .models import Mesa, Reserva

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidad', 'ubicacion', 'activa']
    list_filter = ['activa', 'capacidad']
    search_fields = ['numero', 'ubicacion']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'mesa', 'fecha_reserva', 'hora_reserva', 'numero_personas', 'estado']
    list_filter = ['estado', 'fecha_reserva']
    search_fields = ['cliente__username', 'mesa__numero']
    date_hierarchy = 'fecha_reserva'

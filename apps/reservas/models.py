from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.constants.estados import (
    ESTADOS_MESA, MESA_DISPONIBLE,
    ESTADOS_RESERVA, RESERVA_PENDIENTE
)

Usuario = get_user_model()


class Mesa(models.Model):
    """Modelo para las mesas del restaurante"""
    numero = models.PositiveIntegerField(unique=True, verbose_name="Número de Mesa")
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad (personas)")
    estado = models.CharField(max_length=20, choices=ESTADOS_MESA, default=MESA_DISPONIBLE, verbose_name="Estado")
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    activa = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['numero']
    
    def __str__(self):
        return f"Mesa {self.numero} - {self.capacidad} personas ({self.get_estado_display()})"
    
    def esta_disponible(self):
        """Verifica si la mesa está disponible"""
        return self.estado == MESA_DISPONIBLE and self.activa


class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mesa Asignada")
    fecha_reserva = models.DateTimeField(verbose_name="Fecha de Reserva")
    cantidad_personas = models.PositiveIntegerField(verbose_name="Cantidad de Personas")
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default=RESERVA_PENDIENTE, verbose_name="Estado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']

    def __str__(self):
        return f"Reserva de {self.usuario.get_full_name()} - {self.fecha_reserva.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        if self.fecha_reserva < timezone.now():
            raise ValidationError("No puedes realizar una reserva para una fecha pasada")
        if self.cantidad_personas < 1:
            raise ValidationError("Debes incluir al menos 1 persona")
        if self.cantidad_personas > 20:
            raise ValidationError("El máximo de personas por reserva es 20")

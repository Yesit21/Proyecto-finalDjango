from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

Usuario = get_user_model()


class Mesa(models.Model):
    """Modelo para las mesas del restaurante"""
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    numero = models.PositiveIntegerField(unique=True, verbose_name="Número de mesa")
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad (personas)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado")
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
        return self.estado == 'disponible' and self.activa


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mesa asignada")
    fecha_reserva = models.DateTimeField(verbose_name="Fecha de la reserva")
    cantidad_personas = models.PositiveIntegerField(verbose_name="Cantidad de personas")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
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
            raise ValidationError("No puedes hacer una reserva en una fecha pasada")
        if self.cantidad_personas < 1:
            raise ValidationError("Debe incluir al menos 1 persona")
        if self.cantidad_personas > 20:
            raise ValidationError("El máximo de personas por reserva es 20")

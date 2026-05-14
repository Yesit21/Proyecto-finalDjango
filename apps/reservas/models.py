from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

Usuario = get_user_model()


class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=2)
    ubicacion = models.CharField(max_length=120, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero} ({self.capacidad})"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mesa")
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

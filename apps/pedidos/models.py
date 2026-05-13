from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from core.constants.estados import ESTADOS_PEDIDO


class Pedido(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    reserva = models.OneToOneField('reservas.Reserva', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedido')
    fecha_pedido = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f'Pedido #{self.id} - {self.get_estado_display()}'

    def calcular_total(self):
        return sum(item.subtotal for item in self.items.all())

    def actualizar_total(self):
        self.total = self.calcular_total()
        self.save(update_fields=['total'])


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.SET_NULL, null=True, blank=True)
    plato = models.ForeignKey('menu.Plato', on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.cantidad) * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} x {self.cantidad}'

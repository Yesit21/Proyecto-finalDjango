from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from core.constants.estados import ESTADOS_PEDIDO, PEDIDO_PENDIENTE


class Pedido(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos', verbose_name="Cliente")
    reserva = models.OneToOneField('reservas.Reserva', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedido', verbose_name="Reserva")
    fecha_pedido = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Pedido")
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default=PEDIDO_PENDIENTE, verbose_name="Estado")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total")
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        ordering = ['-fecha_pedido']
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f'Pedido #{self.id} - {self.get_estado_display()}'

    def calcular_total(self):
        return sum(item.subtotal for item in self.items.all())

    def actualizar_total(self):
        self.total = self.calcular_total()
        self.save(update_fields=['total'])


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    producto = models.ForeignKey('inventario.Producto', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Producto")
    plato = models.ForeignKey('menu.Plato', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Plato")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.cantidad) * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} x {self.cantidad}'

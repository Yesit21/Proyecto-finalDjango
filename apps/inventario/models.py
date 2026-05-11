from django.db import models
from django.utils import timezone

TIPO_MOVIMIENTO = [
    ('entrada', 'Entrada'),
    ('salida', 'Salida'),
]


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_actual = models.IntegerField(default=0)
    alerta_stock = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def esta_bajo_stock(self):
        return self.stock_actual <= self.alerta_stock


class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            if self.tipo == 'entrada':
                self.producto.stock_actual += self.cantidad
            else:
                self.producto.stock_actual = max(self.producto.stock_actual - self.cantidad, 0)
            self.producto.save(update_fields=['stock_actual'])

    def __str__(self):
        return f'{self.get_tipo_display()} {self.cantidad} - {self.producto.nombre}'

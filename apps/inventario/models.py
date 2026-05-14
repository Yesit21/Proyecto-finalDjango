from django.db import models
from django.utils import timezone

TIPO_MOVIMIENTO = [
    ('entry', 'Entry'),
    ('exit', 'Exit'),
]


class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Name")
    descripcion = models.TextField(blank=True, verbose_name="Description")
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Price")
    stock_actual = models.IntegerField(default=0, verbose_name="Current Stock")
    alerta_stock = models.PositiveIntegerField(default=5, verbose_name="Stock Alert")

    class Meta:
        ordering = ['nombre']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.nombre

    @property
    def esta_bajo_stock(self):
        return self.stock_actual <= self.alerta_stock


class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos', verbose_name="Product")
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO, verbose_name="Type")
    cantidad = models.PositiveIntegerField(verbose_name="Quantity")
    fecha = models.DateTimeField(default=timezone.now, verbose_name="Date")
    observaciones = models.TextField(blank=True, verbose_name="Observations")

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Inventory Movement"
        verbose_name_plural = "Inventory Movements"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            if self.tipo == 'entry':
                self.producto.stock_actual += self.cantidad
            else:
                self.producto.stock_actual = max(self.producto.stock_actual - self.cantidad, 0)
            self.producto.save(update_fields=['stock_actual'])

    def __str__(self):
        return f'{self.get_tipo_display()} {self.cantidad} - {self.producto.nombre}'

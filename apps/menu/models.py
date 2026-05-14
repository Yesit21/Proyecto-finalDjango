from django.db import models


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    unidad = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    producto_inventario = models.ForeignKey(
        'inventario.Producto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingredientes',
    )

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    CATEGORIA_CHOICES = [
        ('entradas', 'Entradas'),
        ('platos_principales', 'Platos Principales'),
        ('postres', 'Postres'),
        ('bebidas', 'Bebidas'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del plato")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoría")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    imagen = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name="Imagen")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ingredientes = models.ManyToManyField(
        Ingrediente,
        through="PlatoIngrediente",
        related_name="platos",
        blank=True,
    )

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre


class PlatoIngrediente(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    class Meta:
        unique_together = ("plato", "ingrediente")
        verbose_name = "Ingrediente del plato"
        verbose_name_plural = "Ingredientes del plato"

    def __str__(self):
        return f"{self.plato.nombre} - {self.ingrediente.nombre}"


class PrecioPlato(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name="historial_precios")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Precio de plato"
        verbose_name_plural = "Precios de platos"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.plato.nombre} - {self.precio}"

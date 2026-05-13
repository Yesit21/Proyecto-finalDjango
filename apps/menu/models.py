from django.db import models


class Ingrediente(models.Model):
    """Modelo para ingredientes de los platos"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del ingrediente")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    unidad_medida = models.CharField(
        max_length=20,
        choices=[
            ('kg', 'Kilogramos'),
            ('g', 'Gramos'),
            ('l', 'Litros'),
            ('ml', 'Mililitros'),
            ('unidad', 'Unidades'),
        ],
        default='unidad',
        verbose_name="Unidad de medida"
    )
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock actual")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock mínimo")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio unitario")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.unidad_medida})"

    @property
    def stock_bajo(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock_actual <= self.stock_minimo


class Plato(models.Model):
    CATEGORIA_CHOICES = [
        ('entradas', 'Entradas'),
        ('platos_principales', 'Platos Principales'),
        ('postres', 'Postres'),
        ('bebidas', 'Bebidas'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del plato")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Precio")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoría")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    imagen = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name="Imagen")
    ingredientes = models.ManyToManyField(
        Ingrediente,
        through='PlatoIngrediente',
        related_name='platos',
        verbose_name="Ingredientes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre


class PlatoIngrediente(models.Model):
    """Modelo intermedio para la relación Plato-Ingrediente con cantidad"""
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, verbose_name="Plato")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, verbose_name="Ingrediente")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad necesaria")
    
    class Meta:
        verbose_name = "Ingrediente del Plato"
        verbose_name_plural = "Ingredientes del Plato"
        unique_together = ['plato', 'ingrediente']

    def __str__(self):
        return f"{self.plato.nombre} - {self.ingrediente.nombre} ({self.cantidad} {self.ingrediente.unidad_medida})"

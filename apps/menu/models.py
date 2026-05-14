from django.db import models


class Ingrediente(models.Model):
    """Model for dish ingredients"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Ingredient Name")
    descripcion = models.TextField(blank=True, verbose_name="Description")
    unidad_medida = models.CharField(
        max_length=20,
        choices=[
            ('kg', 'Kilograms'),
            ('g', 'Grams'),
            ('l', 'Liters'),
            ('ml', 'Milliliters'),
            ('unit', 'Units'),
        ],
        default='unit',
        verbose_name="Unit of Measure"
    )
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Current Stock")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Minimum Stock")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Unit Price")
    activo = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ingredientes = models.ManyToManyField(
        Ingrediente,
        through="PlatoIngrediente",
        related_name="platos",
        blank=True,
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.unidad_medida})"

    @property
    def stock_bajo(self):
        """Checks if stock is below minimum"""
        return self.stock_actual <= self.stock_minimo


class Plato(models.Model):
    CATEGORIA_CHOICES = [
        ('starters', 'Entradas'),
        ('main_courses', 'Platos Fuertes'),
        ('desserts', 'Postres'),
        ('drinks', 'Bebidas'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Dish Name")
    descripcion = models.TextField(verbose_name="Description")
    precio = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Category")
    disponible = models.BooleanField(default=True, verbose_name="Available")
    imagen = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name="Image")
    ingredientes = models.ManyToManyField(
        Ingrediente,
        through='PlatoIngrediente',
        related_name='platos',
        verbose_name="Ingredients"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre


class PlatoIngrediente(models.Model):
    """Intermediate model for Plato-Ingredient relationship with quantity"""
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, verbose_name="Dish")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, verbose_name="Ingredient")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Required Quantity")
    
    class Meta:
        verbose_name = "Dish Ingredient"
        verbose_name_plural = "Dish Ingredients"
        unique_together = ['plato', 'ingrediente']

    def __str__(self):
        return f"{self.plato.nombre} - {self.ingrediente.nombre} ({self.cantidad} {self.ingrediente.unidad_medida})"

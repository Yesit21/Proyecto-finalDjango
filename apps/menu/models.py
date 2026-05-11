from django.db import models

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

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre

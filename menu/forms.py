from django import forms
from .models import Plato, Categoria, Ingrediente

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'imagen', 'disponible', 'tiempo_preparacion']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'unidad_medida', 'stock_actual', 'stock_minimo', 'precio_unitario']

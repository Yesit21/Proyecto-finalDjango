from django import forms
from .models import Plato, Ingrediente, PlatoIngrediente


class IngredienteForm(forms.ModelForm):
    """Form to create and edit ingredients"""
    
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'descripcion', 'unidad_medida', 'stock_actual', 'stock_minimo', 'precio_unitario', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'e.g. Tomato'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 3,
                'placeholder': 'Ingredient description...'
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'input-field'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-amber-600 focus:ring-2 focus:ring-amber-500'
            })
        }


class PlatoIngredienteForm(forms.ModelForm):
    """Form to add ingredients to a dish"""
    
    class Meta:
        model = PlatoIngrediente
        fields = ['ingrediente', 'cantidad']
        widgets = {
            'ingrediente': forms.Select(attrs={
                'class': 'input-field'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            })
        }


class PlatoForm(forms.ModelForm):
    """
    Form to create and edit menu dishes.
    Supports prices in different currencies.
    """
    
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'disponible', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'placeholder': 'e.g. Burger'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'rows': 4,
                'placeholder': 'Describe the dish...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'placeholder': 'e.g. 25000 (COP) or 12.50 (USD)',
                'step': '0.01',
                'min': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-amber-600 focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'accept': 'image/*'
            })
        }
        help_texts = {
            'precio': 'Enter price without currency symbol. Examples: 25000 (pesos), 12.50 (dollars)',
            'imagen': 'Accepted formats: JPG, PNG, GIF (max. 5MB)'
        }
    
    def clean_precio(self):
        """
        Validates that the price is a positive value.
        Accepts both integer and decimal values.
        """
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('Price must be a positive value.')
        return precio

from django import forms
from .models import Plato, Ingrediente, PlatoIngrediente


class IngredienteForm(forms.ModelForm):
    """Formulario para crear y editar ingredientes"""
    
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'descripcion', 'unidad_medida', 'stock_actual', 'stock_minimo', 'precio_unitario', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ej: Tomate'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 3,
                'placeholder': 'Descripción del ingrediente...'
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
    """Formulario para agregar ingredientes a un plato"""
    
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
    Formulario para crear y editar platos del menú.
    Soporta precios en diferentes monedas (pesos colombianos, dólares, etc.)
    """
    
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'disponible', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'placeholder': 'Ej: Bandeja Paisa'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'rows': 4,
                'placeholder': 'Describe el plato...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white',
                'placeholder': 'Ej: 25000 (COP) o 12.50 (USD)',
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
            'precio': 'Ingrese el precio sin símbolo de moneda. Ejemplos: 25000 (pesos), 12.50 (dólares)',
            'imagen': 'Formatos aceptados: JPG, PNG, GIF (máx. 5MB)'
        }
    
    def clean_precio(self):
        """
        Valida que el precio sea un valor positivo.
        Acepta tanto valores enteros como decimales.
        """
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio debe ser un valor positivo.')
        return precio

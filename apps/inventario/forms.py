from django import forms
from .models import MovimientoInventario, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock_actual', 'alerta_stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
            'alerta_stock': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
        }


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'tipo', 'cantidad', 'observaciones']
        widgets = {
            'producto': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
            'tipo': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
            'observaciones': forms.Textarea(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm', 'rows': 3}),
        }

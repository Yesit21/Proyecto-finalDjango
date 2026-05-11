from django import forms
from .models import MovimientoInventario, Proveedor, OrdenCompra

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['ingrediente', 'tipo', 'cantidad', 'motivo']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion', 'activo']

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'fecha_entrega_estimada', 'notas']
        widgets = {
            'fecha_entrega_estimada': forms.DateInput(attrs={'type': 'date'}),
        }

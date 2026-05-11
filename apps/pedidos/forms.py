from django import forms
from .models import Pedido


class EstadoPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm'}),
        }

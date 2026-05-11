from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_reserva', 'cantidad_personas', 'observaciones']
        widgets = {
            'fecha_reserva': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                }
            ),
            'cantidad_personas': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'min': '1',
                    'max': '20'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Observaciones especiales (opcional)'
                }
            ),
        }


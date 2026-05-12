from django import forms
from django.utils import timezone
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
    
    def clean_fecha_reserva(self):
        """Validar que la fecha de reserva no sea en el pasado"""
        fecha = self.cleaned_data.get('fecha_reserva')
        if fecha and fecha < timezone.now():
            raise forms.ValidationError('No puedes hacer una reserva en una fecha pasada.')
        return fecha
    
    def clean_cantidad_personas(self):
        """Validar que la cantidad de personas esté en el rango permitido"""
        cantidad = self.cleaned_data.get('cantidad_personas')
        if cantidad and cantidad < 1:
            raise forms.ValidationError('Debe incluir al menos 1 persona.')
        if cantidad and cantidad > 20:
            raise forms.ValidationError('El máximo es 20 personas por reserva.')
        return cantidad



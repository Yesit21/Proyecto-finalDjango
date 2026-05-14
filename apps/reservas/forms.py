from django import forms
from django.utils import timezone
from .models import Reserva, Mesa

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_reserva', 'cantidad_personas', 'mesa', 'observaciones']
        widgets = {
            'fecha_reserva': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
                }
            ),
            'cantidad_personas': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'min': '1',
                    'max': '20'
                }
            ),
            'mesa': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'rows': 4,
                    'placeholder': 'Observaciones especiales (opcional)'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar mesas activas y disponibles para el cliente
        self.fields['mesa'].queryset = Mesa.objects.filter(activa=True, estado='disponible')
        self.fields['mesa'].empty_label = "Selecciona una mesa (opcional)"
        self.fields['mesa'].required = False
    
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




class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad', 'estado', 'ubicacion', 'activa']
        widgets = {
            'numero': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'min': '1'
                }
            ),
            'capacidad': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'min': '1',
                    'max': '20'
                }
            ),
            'estado': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
                }
            ),
            'ubicacion': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'placeholder': 'Ej: Terraza, Salón principal, Ventana'
                }
            ),
            'activa': forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-amber-600 bg-gray-100 border-gray-300 rounded focus:ring-amber-500 dark:focus:ring-amber-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                }
            ),
        }


class AsignarMesaForm(forms.ModelForm):
    """Formulario para asignar mesa a una reserva"""
    class Meta:
        model = Reserva
        fields = ['mesa', 'estado']
        widgets = {
            'mesa': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
                }
            ),
            'estado': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo mesas disponibles
        self.fields['mesa'].queryset = Mesa.objects.filter(activa=True, estado='disponible')
        self.fields['mesa'].required = False

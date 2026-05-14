from django import forms
from django.utils import timezone
from .models import Mesa, Reserva


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ["numero", "capacidad", "ubicacion", "activa"]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "capacidad": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "ubicacion": forms.TextInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "activa": forms.CheckboxInput(attrs={"class": "rounded"}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['mesa', 'fecha_reserva', 'cantidad_personas', 'observaciones']
        widgets = {
            'mesa': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                }
            ),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mesa'].queryset = Mesa.objects.filter(activa=True).order_by('numero')
    
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

    def clean(self):
        cleaned_data = super().clean()
        mesa = cleaned_data.get('mesa')
        fecha = cleaned_data.get('fecha_reserva')
        cantidad = cleaned_data.get('cantidad_personas')
        if mesa and cantidad and cantidad > mesa.capacidad:
            self.add_error('cantidad_personas', f'La mesa seleccionada tiene capacidad {mesa.capacidad}.')
        if mesa and fecha:
            existe = (
                Reserva.objects
                .filter(mesa=mesa, fecha_reserva=fecha)
                .exclude(pk=self.instance.pk)
                .exclude(estado='cancelada')
                .exists()
            )
            if existe:
                self.add_error('mesa', 'Esa mesa ya está reservada para esa fecha y hora.')
        return cleaned_data


class ReservaStaffForm(ReservaForm):
    class Meta(ReservaForm.Meta):
        fields = ['mesa', 'estado', 'fecha_reserva', 'cantidad_personas', 'observaciones']
        widgets = {
            **ReservaForm.Meta.widgets,
            'estado': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                }
            ),
        }



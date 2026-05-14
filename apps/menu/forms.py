from django import forms
from .models import Ingrediente, Plato, PlatoIngrediente, PrecioPlato


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ["nombre", "unidad", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "unidad": forms.TextInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "activo": forms.CheckboxInput(attrs={"class": "rounded"}),
        }


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ["nombre", "descripcion", "precio", "categoria", "disponible", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "descripcion": forms.Textarea(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm", "rows": 4}),
            "precio": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "categoria": forms.Select(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "disponible": forms.CheckboxInput(attrs={"class": "rounded"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
        }


class PrecioPlatoForm(forms.ModelForm):
    class Meta:
        model = PrecioPlato
        fields = ["precio", "activo"]
        widgets = {
            "precio": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "activo": forms.CheckboxInput(attrs={"class": "rounded"}),
        }


class PlatoIngredienteForm(forms.ModelForm):
    class Meta:
        model = PlatoIngrediente
        fields = ["ingrediente", "cantidad"]
        widgets = {
            "ingrediente": forms.Select(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
            "cantidad": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300 shadow-sm"}),
        }

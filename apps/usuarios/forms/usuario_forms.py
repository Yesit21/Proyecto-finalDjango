from django import forms
from apps.usuarios.models import Usuario
from core.constants.roles import ROLES

class UsuarioCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-field'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-field'})
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'telefono', 'direccion', 'foto', 'activo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'rol': forms.Select(attrs={'class': 'input-field'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field'}),
            'direccion': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'input-field'}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'telefono', 'direccion', 'foto', 'activo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'rol': forms.Select(attrs={'class': 'input-field'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field'}),
            'direccion': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'input-field'}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }

class UsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

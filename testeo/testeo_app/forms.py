from django import forms
from django.contrib .auth.models import User
from .models import Region, Comuna, TipoInmueble,Usuario,TipoUsuario,Inmueble

"""PERFIL """
class Editar_Perfil(forms.ModelForm):
    class Meta:
        model = Usuario     
        fields = ['rut', 'tipo_usuario', 'direccion', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_usuario'].queryset = TipoUsuario.objects.all()
        
"""Registro"""
class RegistroUsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label="Confirmar contraseña", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirm

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'tipo_usuario', 'direccion', 'telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

"""Buscador"""
class PropertyFilterForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(), required=False, empty_label="Seleccione una región"
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(), required=False, empty_label="Seleccione una comuna"
    )
    tipo_inmueble = forms.ModelChoiceField(
        queryset=TipoInmueble.objects.all(), required=False, empty_label="Seleccione un tipo de inmueble"
    )
    ARRENDADO_CHOICES = [
        ('', 'Seleccione estado de arriendo'),
        ('True', 'Arrendado'),
        ('False', 'No arrendado')
    ]
    arrendado = forms.ChoiceField(choices=ARRENDADO_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass 
        else:
            self.fields['comuna'].queryset = Comuna.objects.none()

"""CREACION DE PROPIEDAD"""

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'direccion', 'depto', 'm2_construidos', 
                  'm2_totales', 'estacionamientos', 'habitaciones', 'banios', 
                  'precio', 'arrendado', 'tipo_inmueble', 'region', 'comuna', 'usuarios']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'depto': forms.TextInput(attrs={'class': 'form-control'}),
            'm2_construidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'estacionamientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'banios': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'arrendado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
            'usuarios': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
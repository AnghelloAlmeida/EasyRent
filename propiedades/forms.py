# propiedades/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Propiedad, Profile  # ¡IMPORTANTE: Asegúrate de importar Propiedad y Profile!


# Formulario para agregar/editar propiedades
class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
            'titulo', 'descripcion', 'direccion', 'ciudad', 'pais',
            'precio', 'num_habitaciones', 'num_banos', 'metros_cuadrados',
            'imagen_principal',  # <--- ¡CORRECCIÓN CLAVE AQUÍ: CAMBIADO DE 'imagen' A 'imagen_principal'!
            'disponible', 'tipo_propiedad',
            'tiene_garaje',
            'caracteristicas_adicionales'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_habitaciones': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'num_banos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'metros_cuadrados': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tipo_propiedad': forms.Select(attrs={'class': 'form-control'}),
            'caracteristicas_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej: Piscina, Jardín, Balcón, Seguridad 24/7'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'pais': 'País',
            'precio': 'Precio ($)',
            'num_habitaciones': 'Número de Habitaciones',
            'num_banos': 'Número de Baños',
            'metros_cuadrados': 'Metros Cuadrados (m²)',
            'imagen_principal': 'Imagen Principal', # <--- ¡Y TAMBIÉN AQUÍ EN LOS LABELS!
            'disponible': 'Disponible para Alquiler/Venta',
            'tipo_propiedad': 'Tipo de Propiedad',
            'tiene_garaje': '¿Tiene Garaje?',
            'caracteristicas_adicionales': 'Características Adicionales',
        }


# Formulario para el registro de usuarios (SignUpView utiliza este)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email


# Formulario para editar el perfil del usuario (datos básicos del User)
class UserProfileForm(forms.ModelForm):
    """
    Formulario para que los usuarios editen su información básica del modelo User de Django.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Excluye al usuario actual para permitir que guarde su propio email sin conflicto
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado por otro usuario.")
        return email

# NUEVO FORMULARIO: Para la foto de perfil
class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para que los usuarios editen su foto de perfil.
    """
    class Meta:
        model = Profile
        fields = ['image'] # Solo el campo de imagen

        labels = {
            'image': 'Foto de Perfil',
        }

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}), # Usar FileInput para la subida de archivos
        }
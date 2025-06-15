# propiedades/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Propiedad # Asegúrate de que Propiedad esté importada

# Formulario para agregar/editar propiedades
class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        # Aquí puedes especificar todos los campos del modelo Propiedad que deseas en el formulario.
        # Basado en tu models.py, incluiría estos campos.
        fields = [
            'titulo', 'descripcion', 'direccion', 'ciudad', 'pais',
            'precio', 'num_habitaciones', 'num_banos', 'metros_cuadrados',
            'imagen', 'disponible', 'tipo_propiedad'
        ]
        # Opcional: Widgets para aplicar clases CSS u otros atributos HTML a los campos
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_habitaciones': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'num_banos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'metros_cuadrados': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tipo_propiedad': forms.Select(attrs={'class': 'form-control'}),
            # 'imagen' y 'disponible' no suelen necesitar widgets personalizados si son FieldFile y CheckboxInput
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
            'metros_cuadrados': 'Metros Cuadrados',
            'imagen': 'Imagen Principal',
            'disponible': 'Disponible para Alquiler/Venta',
            'tipo_propiedad': 'Tipo de Propiedad',
        }


# Formulario para el registro de usuarios (SignUpView utiliza este)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) # El email es un campo adicional que no está por defecto en UserCreationForm

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',) # Añade email, nombre y apellido al formulario de registro

    # Puedes añadir validaciones personalizadas aquí si es necesario
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email


# Formulario para editar el perfil del usuario (nuevo para la funcionalidad de Editar Perfil)
class UserProfileForm(forms.ModelForm):
    """
    Formulario para que los usuarios editen su información básica del modelo User de Django.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] # Campos del modelo User que se pueden editar

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }

        # Opcional: Widgets para personalizar la apariencia de los campos (ej. añadir clases CSS)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar si el email ya existe en otro usuario (excluyendo al usuario actual)
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado por otro usuario.")
        return email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Propiedad # Asegúrate de que tu modelo Propiedad esté importado aquí

# Formulario para el registro de nuevos usuarios
class UserRegisterForm(UserCreationForm):
    # Añadimos el campo de email. Lo hacemos requerido ya que UserCreationForm por defecto
    # no lo incluye de forma obligatoria.
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Tu correo electrónico'})
    )

    class Meta:
        model = User
        # Definimos los campos que se mostrarán en el formulario de registro.
        # 'password' y 'password2' son manejados automáticamente por UserCreationForm.
        fields = ['username', 'email']

    # Opcional: Puedes sobrescribir el método save si necesitas lógica adicional.
    # Por ejemplo, para asegurar que el email se guarda correctamente.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Formulario para agregar y editar propiedades
class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        # Definimos los campos que se mostrarán en el formulario.
        # Excluimos 'propietario', 'disponible' y 'fecha_publicacion' porque se manejan en la vista o automáticamente.
        fields = [
            'titulo',
            'descripcion',
            'direccion',
            'ciudad',
            'pais',
            'precio',
            'num_habitaciones',
            'num_banos',
            'metros_cuadrados',
            'imagen',
            'tipo_propiedad', # Este campo debe coincidir con el campo de tu modelo Propiedad
        ]
        # Widgets para personalizar la apariencia de los campos HTML
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título de la propiedad (ej. Casa Moderna)'}),
            'descripcion': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Descripción detallada de la propiedad...'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección completa (ej. Av. Principal y Calle Secundaria)'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad (ej. Guayaquil)'}),
            'pais': forms.TextInput(attrs={'placeholder': 'País (ej. Ecuador)'}),
            'precio': forms.NumberInput(attrs={'placeholder': 'Ej. 150000.00', 'step': '0.01'}),
            'num_habitaciones': forms.NumberInput(attrs={'placeholder': 'Ej. 3', 'min': '1'}),
            'num_banos': forms.NumberInput(attrs={'placeholder': 'Ej. 2', 'min': '1'}),
            'metros_cuadrados': forms.NumberInput(attrs={'placeholder': 'Ej. 120.50', 'step': '0.01'}),
            # 'imagen' no necesita widget si es ImageField, el navegador se encarga.
            # 'tipo_propiedad' no necesita widget si es CharField con choices, se renderizará como select.
        }
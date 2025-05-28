from rest_framework import serializers
from .models import Propiedad # Importa tu modelo Propiedad
from django.contrib.auth.models import User # Si quieres incluir detalles del usuario

class PropiedadSerializer(serializers.ModelSerializer):
    # Opcional: Si quieres mostrar solo el nombre de usuario del propietario en lugar de su ID
    # propietario_username = serializers.ReadOnlyField(source='propietario.username')

    class Meta:
        model = Propiedad
        # fields = '__all__' # Incluye todos los campos del modelo
        fields = ['id', 'titulo', 'descripcion', 'precio', 'imagen', 'propietario', 'disponible']
        # Si quisieras mostrar el username del propietario en lugar de solo el ID, harías esto:
        # fields = ['id', 'titulo', 'descripcion', 'precio', 'imagen', 'propietario_username', 'disponible']
        # read_only_fields = ['propietario'] # Haz que el propietario sea de solo lectura si lo manejas en la vista

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] # Puedes añadir más campos si los necesitas
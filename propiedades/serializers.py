# propiedades/serializers.py

from rest_framework import serializers
from .models import Propiedad
from django.contrib.auth.models import User

class PropiedadSerializer(serializers.ModelSerializer):
    # Agrega el campo 'owner' como de solo lectura.
    # source='owner.username' asegura que se muestre el nombre de usuario del propietario.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Propiedad
        fields = '__all__' # Incluye todos los campos, incluido 'owner'
        # O podrías especificar explícitamente:
        # fields = ['id', 'owner', 'titulo', 'descripcion', 'precio', 'direccion',
        #           'ciudad', 'pais', 'habitaciones', 'banios',
        #           'metros_cuadrados', 'imagen', 'disponible',
        #           'fecha_publicacion', 'fecha_actualizacion']


class UserSerializer(serializers.ModelSerializer):
    # Relaciona las propiedades con el usuario.
    # many=True indica que un usuario puede tener muchas propiedades.
    # read_only=True asegura que las propiedades no se puedan modificar a través del serializer del usuario.
    propiedades = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'propiedades']
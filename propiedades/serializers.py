# propiedades/serializers.py

from rest_framework import serializers
from .models import Propiedad
from django.contrib.auth.models import User

class PropiedadSerializer(serializers.ModelSerializer):
    # CORRECCIÓN: Usar 'propietario' que es el nombre real del campo en models.py
    propietario = serializers.ReadOnlyField(source='propietario.username')

    class Meta:
        model = Propiedad
        fields = '__all__' # Incluye todos los campos, incluido 'propietario'

class UserSerializer(serializers.ModelSerializer):
    # Relaciona las propiedades con el usuario.
    # many=True indica que un usuario puede tener muchas propiedades.
    # read_only=True asegura que las propiedades no se puedan modificar a través del serializer del usuario.
    # El related_name por defecto para ForeignKey es <model_name>_set, e.g. propiedad_set
    propiedades = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'propiedades']
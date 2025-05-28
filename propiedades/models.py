# propiedades/models.py

from django.db import models
from django.contrib.auth.models import User

# Opcional: Define las opciones para el tipo de propiedad
TIPO_PROPIEDAD_CHOICES = [
    ('casa', 'Casa'),
    ('apartamento', 'Apartamento'),
    ('terreno', 'Terreno'),
    ('local_comercial', 'Local Comercial'),
    ('oficina', 'Oficina'),
    ('otro', 'Otro'),
]

class Propiedad(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='Ecuador') # Puedes mantener un default si es necesario
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    num_habitaciones = models.IntegerField(default=1)
    num_banos = models.IntegerField(default=1)
    metros_cuadrados = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='propiedades_pics/', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    # Nuevo campo para el tipo de propiedad
    tipo_propiedad = models.CharField(
        max_length=50,
        choices=TIPO_PROPIEDAD_CHOICES,
        default='casa'
    )

    def __str__(self):
        return self.titulo
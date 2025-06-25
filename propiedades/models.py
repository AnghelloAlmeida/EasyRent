# propiedades/models.py

from django.db import models
from django.contrib.auth.models import User
from PIL import Image # Importa la biblioteca Pillow para manipulación de imágenes
from django.db.models.signals import post_save # Importa la señal post_save
from django.dispatch import receiver # Importa el decorador receiver

# CHOICES para el tipo de propiedad
TIPO_PROPIEDAD_CHOICES = [
    ('casa', 'Casa'),
    ('apartamento', 'Apartamento'),
    ('terreno', 'Terreno'),
    ('oficina', 'Oficina'),
    ('local_comercial', 'Local Comercial'),
    ('bodega', 'Bodega'),
    ('villa', 'Villa'),
    ('condominio', 'Condominio'),
    ('duplex', 'Dúplex'),
    ('penthouse', 'Penthouses'),
]

class Propiedad(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='Ecuador') # Valor por defecto
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_propiedad = models.CharField(max_length=50, choices=TIPO_PROPIEDAD_CHOICES, default='casa')
    num_habitaciones = models.IntegerField(null=True, blank=True)
    num_banos = models.IntegerField(null=True, blank=True)
    metros_cuadrados = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tiene_garaje = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    disponible = models.BooleanField(default=True)
    imagen_principal = models.ImageField(upload_to='propiedades_pics/', null=True, blank=True)
    caracteristicas_adicionales = models.TextField(blank=True, null=True)

    # Nuevos campos para la integración de IA
    ia_reseña_generada = models.TextField(blank=True, null=True, verbose_name="Reseña IA")
    # CAMBIO AQUÍ: FloatField para permitir decimales en la calificación
    ia_calificacion = models.FloatField(blank=True, null=True, verbose_name="Calificación IA")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Propiedades"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Establece un valor por defecto para 'image' en caso de que no se suba una imagen.
    # Asegúrate de que 'profile_pics/default.jpg' exista en tu MEDIA_ROOT.
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Sobreescribimos el método save para redimensionar la imagen
    def save(self, *args, **kwargs):
        # Primero, guarda la instancia del modelo para que la imagen se suba al sistema de archivos
        super().save(*args, **kwargs)

        try:
            # Abre la imagen usando Pillow desde la ruta guardada
            img = Image.open(self.image.path)

            # Convierte la imagen a modo RGB si es RGBA y se está guardando como JPEG
            # Esto es crucial para manejar la transparencia (RGBA) que JPEG no soporta
            if img.mode == 'RGBA' and self.image.name.lower().endswith(('.jpg', '.jpeg')):
                # Crea una nueva imagen con un fondo blanco
                background = Image.new("RGB", img.size, (255, 255, 255))
                # Pega la imagen RGBA sobre el fondo blanco usando su canal alfa como máscara
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode == 'P' and self.image.name.lower().endswith(('.jpg', '.jpeg')):
                # Convierte de modo paleta (P) a RGB si es necesario para JPEG
                img = img.convert('RGB')


            # Redimensionar la imagen si excede las dimensiones deseadas (300x300)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size) # Redimensiona la imagen in-place

            # Guarda la imagen modificada de nuevo en la misma ruta
            img.save(self.image.path)

        except Exception as e:
            # Captura cualquier error que ocurra durante el procesamiento de la imagen
            # y lo imprime para depuración. Puedes añadir logging aquí si lo prefieres.
            print(f"Error al procesar la imagen de perfil para {self.user.username}: {e}")
            # Si el error persiste, puede que el archivo 'default.jpg' esté corrupto o sea un formato inusual.
            # Asegúrate de que 'default.jpg' sea un JPEG o PNG válido y sin errores.


# Signals para crear y guardar el perfil automáticamente cuando un usuario es creado/actualizado
# Este decorador asegura que la función 'create_profile' se ejecute cada vez que un objeto User es guardado.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Si el usuario es nuevo (created=True), crea un objeto Profile asociado a él.
    if created:
        Profile.objects.create(user=instance)

# Este decorador asegura que la función 'save_profile' se ejecute cada vez que un objeto User es guardado.
# (Se dispara después de que 'create_profile' haya terminado si el usuario es nuevo).
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Solo intentamos guardar el perfil si el usuario ya tiene uno.
    # Esto es una precaución para usuarios existentes que podrían no tener un perfil aún (ej. antes de que se implementara el signal).
    if hasattr(instance, 'profile'):
        instance.profile.save()

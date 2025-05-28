# C:\easyrent_demo\propiedades\admin.py

from django.contrib import admin
from .models import Propiedad

@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ciudad', 'precio', 'propietario', 'disponible', 'fecha_publicacion')
    list_filter = ('disponible', 'ciudad', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion', 'ciudad', 'direccion', 'propietario__username')
    date_hierarchy = 'fecha_publicacion'
    # fields = ('titulo', 'descripcion', 'precio', 'direccion', 'ciudad', 'num_habitaciones', 'num_banos', 'metros_cuadrados', 'imagen', 'disponible', 'propietario')
    # Para hacer el propietario de solo lectura una vez que se crea (o asignarlo automáticamente)
    readonly_fields = ('propietario', 'fecha_publicacion') # Haz que el propietario sea de solo lectura para evitar cambios accidentales

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si el usuario no es superusuario, solo ve sus propias propiedades
        if not request.user.is_superuser:
            qs = qs.filter(propietario=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.pk: # Solo al crear una nueva propiedad
            obj.propietario = request.user # Asigna el propietario al usuario logueado
        super().save_model(request, obj, form, change)
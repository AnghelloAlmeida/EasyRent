# easyrent_demo/urls.py

from django.contrib import admin
from django.urls import path, include # <--- Asegúrate de que 'include' esté importado aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    path('propiedades/', include('propiedades.urls')), # Asumiendo que esta es tu app principal
    path('accounts/', include('django.contrib.auth.urls')), # <--- ¡ESTA ES LA LÍNEA AÑADIDA!
    # Puedes añadir otras URLs de tu proyecto aquí si las tienes
]
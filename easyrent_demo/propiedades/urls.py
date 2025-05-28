from django.urls import path
from .views import agregar_propiedad

urlpatterns = [
    path('agregar/', agregar_propiedad, name='agregar_propiedad'),
]
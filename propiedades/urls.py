# propiedades/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('lista/', views.lista_propiedades_frontend, name='lista_propiedades_frontend'),
    path('lista/ajax/', views.lista_propiedades_ajax, name='lista_propiedades_ajax'),
    path('detalle/<int:pk>/', views.detalle_propiedad_frontend, name='detalle_propiedad_frontend'),
    path('mis-propiedades/', views.mis_propiedades_frontend, name='mis_propiedades_frontend'),
    path('agregar/', views.agregar_propiedad_frontend, name='agregar_propiedad_frontend'),
    path('editar/<int:pk>/', views.editar_propiedad_frontend, name='editar_propiedad_frontend'),
    path('eliminar/<int:pk>/', views.eliminar_propiedad_frontend, name='eliminar_propiedad_frontend'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # --- NUEVA URL PARA LA ESTIMACIÓN DE PRECIOS ---
    path('estimar-precio/', views.estimar_precio_propiedad, name='estimar_precio_propiedad'),
    # -----------------------------------------------
]
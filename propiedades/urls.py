from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URLs públicas
    path('', views.welcome_page, name='welcome_page'),
    path('propiedades/', views.lista_propiedades_frontend, name='lista_propiedades_frontend'),
    path('propiedades/<int:pk>/', views.detalle_propiedad_frontend, name='detalle_propiedad_frontend'),

    # NUEVA URL PARA EL DASHBOARD DEL USUARIO
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),

    # URLs de autenticación
    path('register/', views.SignUpView.as_view(), name='register'), # <-- Esta es la URL que tu error buscaba
    # Modificamos LoginView para redirigir al dashboard después del login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page='user_dashboard'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome_page'), name='logout'),

    # URLs para usuarios autenticados
    path('mis-propiedades/', views.mis_propiedades_frontend, name='mis_propiedades_frontend'),
    path('agregar-propiedad/', views.agregar_propiedad_frontend, name='agregar_propiedad_frontend'),
    path('propiedades/<int:pk>/editar/', views.editar_propiedad_frontend, name='editar_propiedad_frontend'),
    path('propiedades/<int:pk>/eliminar/', views.eliminar_propiedad_frontend, name='eliminar_propiedad_frontend'),
]
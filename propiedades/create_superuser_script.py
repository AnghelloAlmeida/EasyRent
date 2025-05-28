import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrent_demo.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Define los datos del superusuario
username = 'Fernando'  # Puedes cambiar este nombre de usuario
email = 'fernando@gmail.com'  # Puedes cambiar este correo electrónico
password = 'fernando2004'  # ¡CAMBIA ESTA CONTRASEÑA POR UNA SEGURA!

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superusuario '{username}' creado exitosamente.")
    else:
        print(f"El superusuario '{username}' ya existe.")
except Exception as e:
    print(f"Ocurrió un error al crear el superusuario: {e}")
# easyrent_demo/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv # ### NUEVA LÍNEA ###

# Carga las variables de entorno desde el archivo .env al inicio del script.
# Se espera que el archivo .env esté en la raíz del proyecto.
load_dotenv() # ### NUEVA LÍNEA ###


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j%e8m!m@t7x)57h8g3160e=36z$l*v%41c7b5-g6g7(j@l4n7z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # ¡IMPORTANTE: debe estar antes de django.contrib.admin para que Jazzmin funcione correctamente!
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'propiedades', # Tu aplicación de propiedades
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'easyrent_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Directorio para templates globales del proyecto
        'APP_DIRS': True, # Crucial para que Django busque templates dentro de cada aplicación (incluyendo Jazzmin y propiedades)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # Si tienes custom_tags, asegúrate de que esta sección esté descomentada y la ruta sea correcta
            # 'libraries': {
            #     # 'custom_tags': 'propiedades.templatetags.custom_tags', # Si necesitas esto, descomenta y asegura que la ruta es correcta
            # }
        },
    },
]

WSGI_APPLICATION = 'easyrent_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#password-validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es' # Cambiado a español de España

TIME_ZONE = 'America/Guayaquil' # Zona horaria de Ecuador (Guayaquil)

USE_I18N = True # Habilita el sistema de traducción de Django

# USE_L10N está obsoleto a partir de Django 4.0+.
# Su funcionalidad ahora está implicada por USE_TZ. Puedes dejarlo o quitarlo.
# USE_L10N = True

USE_TZ = True # Habilita el soporte para zonas horarias


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Directorio donde 'collectstatic' recolectará todos los archivos estáticos en producción
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Directorio(s) donde Django buscará archivos estáticos durante el desarrollo
]

# Media files (for user uploads like property images)
MEDIA_URL = '/media/' # URL para servir archivos subidos por el usuario
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Directorio donde se guardarán los archivos subidos


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom authentication redirects
LOGIN_REDIRECT_URL = 'user_dashboard' # URL a la que se redirige después de un inicio de sesión exitoso
LOGOUT_REDIRECT_URL = 'welcome_page' # URL a la que se redirige después de un cierre de sesión exitoso
LOGIN_URL = 'login' # La URL para el inicio de sesión (usado por @login_required, etc.)


# ====================================================================
# EMAIL CONFIGURATION FOR PASSWORD RESET (Y OTROS EMAILS)
# ====================================================================

# Para DESARROLLO/PRUEBAS: Ver emails en la consola (NO envía correos reales)
# Descomenta la línea de abajo y *comenta* todas las líneas de EMAIL_HOST, EMAIL_PORT, etc., si quieres usar este backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Para ENVÍO REAL DE EMAILS (usando SMTP, por ejemplo con Gmail)
# IMPORTANTE: En producción, considera servicios dedicados como SendGrid, Mailgun, AWS SES.
# Las credenciales de Gmail son solo para desarrollo/pruebas por las limitaciones y seguridad.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True # Usa TLS para la seguridad de la conexión (recomendado con puerto 587)
# EMAIL_USE_SSL = False # No uses SSL si usas TLS en el puerto 587. Solo si el puerto es 465 (generalmente con SSL)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ATENCIÓN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES REALES DE GMAIL (O TU PROVEEDOR SMTP)
# Para Gmail, necesitas una 'Contraseña de Aplicación' (App Password), NO tu contraseña normal de Gmail.
# Asegúrate de tener la Verificación en Dos Pasos activada en tu cuenta de Google para poder generarla.
EMAIL_HOST_USER = '21anghello21@gmail.com'
EMAIL_HOST_PASSWORD = 'utqkawqvzenfoddz' # <--- ¡TU CONTRASEÑA DE APLICACIÓN DE 16 CARACTERES SIN ESPACIOS!
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# El correo que aparecerá como remitente. Debe ser un correo válido y,
# preferiblemente, el mismo que EMAIL_HOST_USER o un alias autorizado.
DEFAULT_FROM_EMAIL = 'no-reply@easyrent.com'

# Si quieres que los errores de envío de email no detengan tu aplicación,
# cámbialo a True. En desarrollo, False es útil para ver los errores y depurar.
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_TIMEOUT = 5 # Timeout en segundos para operaciones de email


# ------------------------------------------------------------------
# CONFIGURACIÓN DE JAZZMIN
# ------------------------------------------------------------------

JAZZMIN_SETTINGS = {
    # Título y encabezado del sitio admin
    "site_title": "EasyRent Admin",
    "site_header": "EasyRent",
    "site_brand": "EasyRent", # Texto de la marca en la barra lateral
    "site_logo": None, # Ruta a un logo, e.g., "static/img/logo.png"
    "login_logo": None, # Logo para la página de login
    "login_logo_dark": None,
    "site_logo_classes": "img-circle", # Clases CSS para el logo (opcional)
    "welcome_sign": "Bienvenido al panel de administración de EasyRent", # Mensaje en la página de login
    "copyright": "EasyRent Ltda.", # Texto de copyright en el pie de página
    "search_model": ["auth.User", "propiedades.Propiedad"], # Modelos que se pueden buscar globalmente
    "site_url": "/", # URL a la que el logo y el "Ver Sitio" apuntan

    # Navegación y menú superior
    "topmenu_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Sitio", "url": "welcome_page"}, # Asegúrate de que 'welcome_page' esté definida en tus urls.py
        {"model": "auth.User"}, # Enlace directo al modelo User
        {"app": "propiedades"}, # Enlace directo a la aplicación propiedades
    ],

    "navigation_expanded": True, # Sidebar expandido por defecto
    "hide_apps": [], # Lista de nombres de apps a ocultar del sidebar
    "hide_models": [], # Lista de strings de modelos ('app_label.model_name') a ocultar

    # Estilos del sidebar
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True, # Estilo plano de navegación en el sidebar

    # Iconos para modelos y apps (usa Font Awesome 5 Free)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "propiedades.Propiedad": "fas fa-home",
        "propiedades.Profile": "fas fa-address-card",
    },
    "default_icon_parents": "fas fa-chevron-circle-right", # Icono por defecto para apps/modelos padre
    "default_icon_children": "fas fa-circle", # Icono por defecto para modelos hijos

    # Formatos de formulario de cambio
    "changeform_format": "horizontal_tabs", # Los campos del formulario se organizan en pestañas horizontales
    "changeform_format_overrides": {"auth.user": "vertical_tabs"}, # Sobrescribe el formato para el modelo User

    # CSS y JS personalizados
    "custom_css": "admin/css/my_jazzmin_theme.css", # Ruta a tu CSS personalizado para el admin
    "custom_js": None, # Ruta a tu JS personalizado para el admin

    "show_ui_builder": True, # Permite usar el UI Builder de Jazzmin para ajustar el tema visualmente
}


JAZZMIN_UI_TWEAKS = {
    # Opciones de tamaño de texto
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "sidebar_nav_small_text": False,

    # Colores y estilo de la barra de navegación
    "brand_colour": "navbar-success", # Color para el área de la marca
    "accent": "accent-success", # Color de acento para elementos interactivos
    "navbar": "navbar-dark", # Estilo de la barra de navegación
    "no_navbar_border": False,
    "navbar_fixed": True, # Fija la barra de navegación en la parte superior

    # Diseño general
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True, # Fija el sidebar

    # Estilos adicionales del sidebar
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True, # Indenta los elementos hijos en el sidebar
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,

    # Tema de AdminLTE (elegido de los disponibles)
    "theme": "flatly", # Un tema base limpio y moderno
    "dark_mode_theme": None, # Puedes configurar un tema oscuro si lo deseas, e.g., "darkly"

    # Clases CSS para botones
    "button_classes": {
        "primary": "btn-outline-success",
        "secondary": "btn-outline-info",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_button_classes": {
        "overview": "btn-primary",
        "add": "btn-success",
        "change": "btn-info",
        "delete": "btn-danger"
    }
}

# ------------------------------------------------------------------
# FIN DE LA CONFIGURACIÓN DE JAZZMIN
# ------------------------------------------------------------------


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ATENCIÓN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# CONFIGURACIÓN DE LA CLAVE API DE GOOGLE GEMINI
# Se obtiene del archivo .env para mayor seguridad.
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # ### NUEVA LÍNEA ###

# Opcional: Asegurarse de que la clave se ha cargado (útil para depuración)
if not GOOGLE_API_KEY and not DEBUG: # Solo lanzará error si no está en producción
    raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada. ¡Es requerida para la funcionalidad de IA!") # ### NUEVA LÍNEA ###
# **Aplicación de Gestión de Propiedades EasyRent**

## **Integrantes**
- [Anghello Almeida]
- [Erick Terranova] Lider

## **Descripción de Funcionalidades**
EasyRent es una aplicación robusta diseñada para optimizar la gestión de propiedades inmobiliarias. Solo necesitas ingresar los detalles de la propiedad, y la aplicación te **asistirá en la creación de** reseñas atractivas y **te ofrecerá una estimación de precio** (simulada), simplificando el proceso.

Las funcionalidades principales incluyen:

- **Gestión Integral de Propiedades**: Permite a los usuarios crear, visualizar, editar y eliminar listados de propiedades con todos sus detalles.
- **Asistencia en la Creación de Reseñas**: Hemos incorporado una funcionalidad que **sugiere y ayuda a redactar** reseñas textuales descriptivas y persuasivas para cada propiedad, **buscando elevar la calidad** de los anuncios que el usuario finaliza.
- **Herramienta de Estimación de Precio (Simulada)**: Ofrece un módulo que **apoya al usuario en la estimación** del precio de la propiedad, proporcionando un cálculo de referencia basado en sus características clave para guiar la decisión.
- **Autenticación y Autorización de Usuarios**: Sistema completo de registro, inicio de sesión y control de acceso seguro.
- **Restablecimiento de Contraseña Vía Email**: Funcionalidad segura para que los usuarios puedan recuperar el acceso a sus cuentas.
- **Gestión de Imágenes de Propiedades**: Permite subir y asociar múltiples fotografías a cada propiedad.
- **Panel de Administración Moderno (Jazzmin)**: Interfaz de administración de Django estéticamente agradable y personalizable.

## **Tecnologías**

### **Backend:**
- Django: Framework web de Python para un desarrollo rápido y seguro.
- Python: Lenguaje de programación principal del backend.
- SQLite: Base de datos por defecto para desarrollo (se recomienda PostgreSQL para producción).
- Google Gemini API: Utilizada para **procesamiento y sugerencia de texto**, como el enriquecimiento de descripciones de propiedades.
- `python-dotenv`: Para la gestión segura de variables de entorno.
- Django Jazzmin: Panel de administración personalizable.
- Servicio SMTP (Gmail): Para el envío de correos electrónicos.

### **Frontend:**
- HTML: Lenguaje de marcado estándar para la estructura de la web.
- CSS: Para el diseño y estilo visual de la aplicación.
- Bootstrap: Framework CSS para un diseño responsivo.
- JavaScript: Para interactividad y funcionalidades dinámicas.

## **Instrucciones de Instalación y Ejecución**

### **Prerrequisitos**
- Python: Asegúrate de tener Python instalado en tu sistema. Se recomienda la versión 3.9.11 o superior. Puedes descargarlo desde [https://www.python.org/](https://www.python.org/).

### **Configuración de Variables de Entorno**

El proyecto EasyRent utiliza variables de entorno para almacenar configuraciones sensibles (claves API, credenciales de correo, etc.). Estas variables se leen desde un archivo `.env`.

1.  Crea un archivo llamado `.env` en la **raíz de tu proyecto** (al mismo nivel que `manage.py`).

2.  Añade las siguientes variables a tu archivo `.env`, reemplazando los valores de ejemplo con tus propias credenciales y configuraciones:

    SECRET_KEY="tu_clave_secreta_django_aqui_generada_aleatoriamente_por_favor"
    GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    EMAIL_HOST_USER="tu.correo.app@gmail.com"
    EMAIL_HOST_PASSWORD="tupassworddeaplicacionde16digitos"
    DEBUG=True
    ALLOWED_HOSTS="127.0.0.1,localhost"
   
    Es **IMPRESCINDIBLE** que añadas `/.env` a tu archivo `.gitignore`. Esto previene que tus credenciales sensibles se suban accidentalmente a repositorios públicos.

### **Pasos de Instalación**

1.  **Clona el Repositorio**:
    Para comenzar, necesitarás obtener una copia local del código del proyecto. Abre tu terminal o línea de comandos y ejecuta:

    git clone [https://gitlab.com/tu-usuario/easyrent.git](https://gitlab.com/tu-usuario/easyrent.git) # Reemplaza con la URL REAL de tu repositorio

2.  **Accede al Directorio del Proyecto**:
    Una vez clonado, navega al directorio raíz del proyecto EasyRent:

    cd easyrent_demo # Asegúrate de que este sea el nombre correcto de tu carpeta raíz


3.  **Crea y Activa un Entorno Virtual**:
    Un entorno virtual es fundamental para aislar las dependencias del proyecto y evitar conflictos con otras instalaciones de Python.


    python -m venv venv

    Para Windows:

    .\venv\Scripts\activate

    Para macOS/Linux:

    source venv/bin/activate

    (Deberías ver `(venv)` al inicio de tu línea de comandos, indicando que el entorno virtual está activo).

4.  **Instala las Dependencias**:
    Con el entorno virtual activado, instala todas las librerías y paquetes necesarios listados en `requirements.txt`:


    pip install -r requirements.txt

5.  **Aplica las Migraciones de la Base de Datos**:
    Django utiliza migraciones para gestionar los cambios en el esquema de la base de datos.

    python manage.py makemigrations propiedades # Esto puede variar si tu app principal tiene otro nombre
    python manage.py makemigrations # Ejecuta para otras apps si hay cambios pendientes
    python manage.py migrate # Aplica todas las migraciones a la base de datos
    

6.  **Crea un Superusuario (Administrador)**:
    Necesitarás un usuario con privilegios de administrador para acceder al panel de administración de Django.

    python manage.py createsuperuser
    
    Sigue las instrucciones en pantalla para ingresar el nombre de usuario, dirección de correo electrónico y contraseña.

### **Ejecución del Proyecto**

1.  **Inicia el Servidor de Desarrollo**:
    Finalmente, inicia el servidor de desarrollo de Django:

    python manage.py runserver

    Si todo se configuró correctamente, verás un mensaje en la terminal indicando que el servidor está escuchando en `http://127.0.0.1:8000/`.

2.  **Accede a la Aplicación**:
    - Abre tu navegador web y visita: `http://127.0.0.1:8000/`. Esta es la interfaz principal de la aplicación EasyRent.
    - Accede al panel de administración: `http://127.0.0.1:8000/admin/`. Utiliza las credenciales del superusuario que creaste para iniciar sesión.

## **Uso**

1.  Accede a la aplicación: Abre tu navegador web y navega a `http://127.0.0.1:8000`. Podrás explorar las propiedades o iniciar sesión/registrarte.
2.  Publica una nueva propiedad: Si eres un usuario registrado, puedes ir a la sección de "Agregar Propiedad" (en el frontend o admin). Rellena los detalles, incluyendo una descripción.
3.  Generación de Reseñas por IA: Una vez que la propiedad se guarda, la aplicación usará la descripción para interactuar con Google Gemini API, generando automáticamente una reseña y una calificación.
4.  Visualiza las reseñas: La reseña y calificación generadas por IA se mostrarán en la página de detalles de la propiedad.

## **Estructura del Proyecto**

easyrent_demo/                  # Carpeta raíz del proyecto Django
├── .vscode/                    # Configuración para Visual Studio Code
├── __pycache__/               # Archivos .pyc compilados por Python
├── .env                       # Variables de entorno sensibles (¡agregar a .gitignore!)
├── .gitignore                 # Archivos/carpetas ignorados por Git
├── db.sqlite3                 # Base de datos SQLite (solo desarrollo)
├── manage.py                  # Utilidad de Django para administración del proyecto
├── requirements.txt           # Lista de dependencias del proyecto

├── easyrent_demo/             # Configuración principal del proyecto
│   ├── __init__.py
│   ├── asgi.py                # Entrada para servidores ASGI
│   ├── settings.py            # Configuración global del proyecto
│   ├── urls.py                # URLs raíz del proyecto
│   └── wsgi.py                # Entrada para servidores WSGI

├── propiedades/               # Aplicación principal: gestión de propiedades
│   ├── __init__.py
│   ├── admin.py               # Registro de modelos para el admin
│   ├── apps.py                # Configuración de la app
│   ├── models.py              # Definición de modelos de base de datos
│   ├── views.py               # Lógica de negocio y vistas
│   ├── urls.py                # Rutas URL propias de la app
│   ├── tests.py               # Pruebas unitarias
│   ├── ai_generator.py        # Integración con Google Gemini API
│   ├── price_estimator.py     # Simulación de precios de propiedades
│   └── migrations/            # Migraciones de base de datos
│       ├── __init__.py
│       ├── 0001_initial.py
│       └── 0002_auto_yyyymmdd_xxxx.py

│   ├── static/
│   │   └── propiedades/
│   │       ├── css/
│   │       ├── js/
│   │       └── img/

│   └── templates/
│       └── propiedades/
│           ├── _propiedades_list_partial.html
│           ├── agregar_propiedad.html
│           ├── base.html
│           ├── detalle_propiedad.html
│           ├── edit_profile.html
│           ├── editar_propiedad.html
│           ├── eliminar_propiedad.html
│           ├── estimar_precio.html
│           ├── lista_propiedades.html
│           ├── mis_propiedades.html
│           ├── user_dashboard.html
│           └── welcome_page.html

├── static/                    # Archivos estáticos globales del proyecto
│   └── easyrent_demo/
│       ├── css/
│       ├── js/
│       ├── img/
│       └── fonts/             # (opcional)

├── templates/                 # Plantillas HTML globales
│   └── easyrent_demo/
│       ├── base.html
│       └── registration/
│           ├── login.html
│           ├── register.html
│           ├── password_reset_form.html
│           ├── password_reset_done.html
│           ├── password_reset_email.html
│           ├── password_reset_confirm.html
│           ├── password_reset_complete.html
│           ├── password_change_form.html
│           └── password_change_done.html

├── media/                     # Archivos subidos por usuarios
│   ├── propiedades/
│   ├── avatars/
│   └── documentos/

└── venv/                      # Entorno virtual (¡no versionar!)

## **Contribuir**

¡Nos encantaría contar con tu ayuda para mejorar EasyRent! Ya seas desarrollador, diseñador, o simplemente alguien apasionado por la tecnología aplicada al sector inmobiliario, tu participación es invaluable. Puedes contribuir de las siguientes maneras:

* **Reporta Bugs**: Si descubres cualquier problema o error en la aplicación, por favor crea una [issue detallada en nuestro repositorio de Github](https://github.com/AnghelloAlmeida/EasyRent.git).
* **Sugerencias**: Si tienes ideas para nuevas funcionalidades o mejoras, abre una [issue](https://github.com/AnghelloAlmeida/EasyRent.git) para compartir tus pensamientos.
* **Git pull**: Si has implementado nuevas características o corregido errores, no dudes en enviar un *Git pull*.

Juntos podemos hacer que EasyRent sea una plataforma más robusta y eficiente para la comunidad.

## **Código de Conducta**

Este proyecto se rige por un [Código de Conducta](CODE_OF_CONDUCT.md). Nos comprometemos a fomentar un ambiente de colaboración abierto, inclusivo y respetuoso para todos los participantes.

## **Licencia**

Este proyecto está bajo la [Licencia MIT](LICENSE). Eres libre de usarlo, copiarlo, modificarlo y distribuirlo, siempre que se incluya el aviso de copyright y la licencia. Siéntete libre de utilizarlo y adaptarlo a tus necesidades.

## **Contacto**

Para cualquier duda o comentario, por favor utiliza la siguiente dirección de correo electrónico:

aalmeidac7@unemi.edu.ec

## **Créditos**

Agradecimiento especial a todos los colaboradores y miembro (Erick Terranova y Anghello Almeida) de la comunidad que han dedicado su tiempo y esfuerzo a este proyecto, aportando ideas, código y apoyo.

También agradecemos a las diversas herramientas y proyectos de código abierto que han sido fundamentales para el desarrollo de EasyRent, incluyendo:

* Django Framework
* Google Gemini API
* Bootstrap
* Django Jazzmin
* Python-dotenv
* Y a la comunidad de Python y Django en general.

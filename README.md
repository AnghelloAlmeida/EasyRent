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

- easyrent_demo/ (Carpeta raíz del proyecto Django)
    - .vscode/: Carpeta de configuración para el editor Visual Studio Code.
    - `__pycache__/`: Carpeta generada automáticamente por Python para almacenar archivos compilados de bytes.
    - `.env`: Archivo para almacenar variables de entorno sensibles (claves API, contraseñas de DB, etc.). **Importante: ¡Debe estar en `.gitignore`!**
    - `.gitignore`: Archivo para especificar qué archivos y carpetas debe ignorar Git (ej., `.env`, `__pycache__`, `venv/`, `media/`).
    - `db.sqlite3`: Base de datos predeterminada de SQLite para desarrollo. No debe versionarse en producción.
    - `manage.py`: Utilidad de línea de comandos de Django para interactuar con el proyecto (ej., `runserver`, `makemigrations`, `migrate`, `createsuperuser`).
    - `requirements.txt`: Lista de todas las dependencias de Python del proyecto (librerías y paquetes).

    - `easyrent_demo/` (Carpeta de configuración principal del proyecto Django)
        - `__init__.py`: Indica a Python que este directorio es un paquete.
        - `asgi.py`: Un punto de entrada compatible con ASGI para servidores web asíncronos. (Para despliegue, si se usa).
        - `settings.py`: Contiene la configuración global del proyecto (base de datos, aplicaciones instaladas, configuraciones de seguridad, claves API generales, etc.).
        - `urls.py`: Define las URL principales de todo el proyecto, que luego pueden incluir las URLs de cada aplicación.
        - `wsgi.py`: Un punto de entrada compatible con WSGI para servidores web. (Para despliegue).

- `propiedades/` (Aplicación Django para la gestión de propiedades)
    - `__init__.py`: Indica que `propiedades` es un paquete Python.
    - `admin.py`: Registra los modelos de la aplicación para que sean accesibles y gestionables desde el panel de administración de Django (Django Admin/Jazzmin).
    - `apps.py`: Contiene la configuración de la aplicación `propiedades`.
    - `models.py`: Define los modelos de datos para las propiedades, usuarios, reseñas, etc., que se mapean a tablas en la base de datos.
    - `views.py`: Contiene la lógica de negocio y las vistas que procesan las solicitudes HTTP y devuelven respuestas (HTML, JSON).
    - `urls.py`: Define las rutas URL específicas para la aplicación `propiedades`.
    - `tests.py`: Contiene las pruebas unitarias y de integración para las funcionalidades de la aplicación.
    - `ai_generator.py`: Módulo que integra la lógica de la API de Google Gemini para la generación de reseñas inteligentes.
    - `price_estimator.py`: Módulo que implementa la lógica de simulación para la estimación de precios de propiedades.
    - `migrations/` (Carpeta para los archivos de migración de la base de datos)
        - `__init__.py`: Indica que es un paquete.
        - `0001_initial.py`: Archivos generados por Django para aplicar cambios al esquema de la base de datos.
        - `0002_auto_yyyymmdd_xxxx.py`: Ejemplo de migración adicional.
        - ...otros archivos de migración generados automáticamente...

    - `static/` (Carpeta para archivos estáticos específicos de la aplicación `propiedades`)
        - `propiedades/` (Subcarpeta para evitar conflictos)
            - `css/`: Contiene archivos CSS específicos para las propiedades (ej., `propiedades.css`, `form_styles.css`).
            - `js/`: Contiene archivos JavaScript específicos para las propiedades (ej., `propiedades.js`, `map_integrations.js`).
            - `img/`: Contiene imágenes específicas de la interfaz de propiedades (ej., `placeholder.png`, `icono_mapa.svg`).

    - `templates/` (Carpeta para las plantillas HTML específicas de la aplicación `propiedades`)
        - `propiedades/` (Subcarpeta para evitar conflictos de nombres con otras apps)
            - `_propiedades_list_partial.html`: Plantilla parcial para mostrar una lista de propiedades.
            - `agregar_propiedad.html`: Plantilla para el formulario de creación de nuevas propiedades.
            - `base.html`: Plantilla base para las páginas de la aplicación `propiedades`.
            - `detalle_propiedad.html`: Plantilla para mostrar los detalles de una propiedad individual.
            - `edit_profile.html`: Plantilla para el formulario de edición del perfil de usuario.
            - `editar_propiedad.html`: Plantilla para el formulario de edición de propiedades existentes.
            - `eliminar_propiedad.html`: Plantilla para la confirmación de eliminación de una propiedad.
            - `estimar_precio.html`: Plantilla para la funcionalidad de estimación de precios.
            - `lista_propiedades.html`: Plantilla para mostrar un listado general de propiedades.
            - `mis_propiedades.html`: Plantilla para mostrar las propiedades del usuario actual.
            - `user_dashboard.html`: Plantilla para el panel de control del usuario.
            - `welcome_page.html`: Plantilla para la página de bienvenida de la aplicación.


- `static/` (Carpeta centralizada para archivos estáticos globales del proyecto)
    - `easyrent_demo/` (Subcarpeta para evitar conflictos y organizar archivos estáticos globales)
        - `css/`: Contiene archivos CSS globales (ej., `base.css`, `main.css`, `bootstrap_custom.css`).
        - `js/`: Contiene archivos JavaScript globales (ej., `global.js`, `animations.js`, `jquery.min.js`).
        - `img/`: Contiene imágenes globales del sitio (ej., `logo.png`, `favicon.ico`, `background.jpg`).
        - `fonts/`: (Opcional) Carpeta para fuentes personalizadas (ej., `font_awesome.woff2`).

- `templates/` (Carpeta centralizada para plantillas HTML globales o base del proyecto)
    - `easyrent_demo/` (Subcarpeta para organizar plantillas base y globales del proyecto)
        - `base.html`: Plantilla base principal que define la estructura HTML común a todas las páginas (head, body, etc.).
        - `registration/` (Carpeta para plantillas de autenticación/registro)
            - `login.html`: Plantilla para el formulario de inicio de sesión.
            - `register.html`: Plantilla para el formulario de registro de usuarios.
            - `password_reset_form.html`: Plantilla para el formulario de solicitud de restablecimiento de contraseña.
            - `password_reset_done.html`: Plantilla de confirmación de envío de email de restablecimiento.
            - `password_reset_email.html`: Plantilla para el contenido del email de restablecimiento.
            - `password_reset_confirm.html`: Plantilla para el formulario de confirmación de nueva contraseña.
            - `password_reset_complete.html`: Plantilla de confirmación de restablecimiento completado.
            - `password_change_form.html`: Plantilla para el formulario de cambio de contraseña.
            - `password_change_done.html`: Plantilla de confirmación de cambio de contraseña realizado.
        - ...otras plantillas HTML comunes o de autenticación/autorización...

- `media/` (Carpeta para archivos subidos por los usuarios, como imágenes de propiedades)
    - `propiedades/`: Almacena las imágenes específicas de las propiedades subidas por los usuarios (ej., `casa_montana_1.jpg`, `apartamento_ciudad_2.jpeg`).
    - `avatars/`: Almacena imágenes de perfil o avatares de usuario (ej., `usuario_juan.png`, `avatar_generico.jpg`).
    - `documentos/`: (Opcional) Almacena documentos subidos relacionados con propiedades o usuarios (ej., `contrato_alquiler.pdf`).
    - ...otras subcarpetas para tipos específicos de archivos subidos...

- `venv/` (Carpeta del entorno virtual de Python, generada al crear el entorno)
    - Contiene todas las librerías y dependencias de Python instaladas específicamente para este proyecto. **¡No debe subirse al control de versiones!**

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

import os
import sys
import django
from django.conf import settings
from dotenv import load_dotenv # ¡NUEVA IMPORTACIÓN!

# Obtener la ruta del directorio del script
script_dir = os.path.dirname(__file__)
# Obtener la ruta del directorio raíz del proyecto (el padre del directorio 'scripts')
project_root = os.path.abspath(os.path.join(script_dir, '..'))
# Obtener la ruta del directorio raíz de easyrent_demo para encontrar .env
easyrent_demo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

# Carga las variables de entorno desde el archivo .env en la raíz del proyecto.
# Esto es crucial para scripts que pueden ejecutarse fuera del entorno de manage.py runserver.
load_dotenv(os.path.join(easyrent_demo_root, '.env')) # ¡NUEVA LÍNEA!

# Añadir la ruta raíz del proyecto al sys.path para que Django pueda encontrar los settings
sys.path.append(project_root)

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrent_demo.settings')
django.setup()

# Importar el SDK de Google Generative AI
import google.generativeai as genai # ¡NUEVA IMPORTACIÓN!

# --- Configuración de la API de Gemini ---
# Obtener la clave API de las variables de entorno.
# Es fundamental que GOOGLE_API_KEY esté definida en tu archivo .env
API_KEY = os.environ.get('GOOGLE_API_KEY')

if not API_KEY:
    raise ValueError("La variable de entorno 'GOOGLE_API_KEY' no está configurada. "
                     "Asegúrate de tenerla en tu archivo .env en la raíz de easyrent_demo.")

genai.configure(api_key=API_KEY) # ¡NUEVA LÍNEA!
# --- FIN Configuración de la API de Gemini ---


# A PARTIR DE AQUÍ TU CÓDIGO ORIGINAL, CON LA LÓGICA DE IA DE GEMINI INTEGRADA
from propiedades.models import Propiedad

def generate_ia_review_and_rating(property_data):
    """
    Genera una reseña y una calificación de IA para una propiedad utilizando Google Gemini.
    """
    titulo = property_data.get('titulo', 'una propiedad')
    descripcion = property_data.get('descripcion', '')
    ciudad = property_data.get('ciudad', 'una ciudad atractiva')
    tipo_propiedad = property_data.get('tipo_propiedad', 'propiedad')
    num_habitaciones = property_data.get('num_habitaciones', 0)
    num_banos = property_data.get('num_banos', 0)
    metros_cuadrados = property_data.get('metros_cuadrados', 0)
    tiene_garaje = "sí" if property_data.get('tiene_garaje') else "no"
    caracteristicas_adicionales = property_data.get('caracteristicas_adicionales', '')

    # Construye el prompt para Gemini
    prompt = f"""Genera una reseña elogiosa y atractiva de una propiedad inmobiliaria en español, de unas 120-180 palabras, destacando sus características y su atractivo en {ciudad}. Menciona el tipo de propiedad, habitaciones, baños y si tiene garaje. Luego, al final de la reseña, en una LÍNEA SEPARADA, proporciona una calificación numérica del 1 al 5 (puedes usar decimales como 4.5), prefijo 'Calificación:'.

    ---
    Detalles de la Propiedad:
    Título: {titulo}
    Descripción: {descripcion}
    Ciudad: {ciudad}
    Tipo: {tipo_propiedad}
    Habitaciones: {num_habitaciones}
    Baños: {num_banos}
    Metros Cuadrados: {metros_cuadrados}
    Garaje: {tiene_garaje}
    Características Adicionales: {caracteristicas_adicionales if caracteristicas_adicionales else 'Ninguna.'}
    ---
    Ejemplo de formato de salida:
    Esta maravillosa propiedad...
    Calificación: 4.8
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        # Puedes ajustar generation_config para controlar la creatividad, etc.
        # response = model.generate_content(prompt, generation_config={"temperature": 0.7})
        response = model.generate_content(prompt)
        generated_text = response.text.strip()

        ia_review = generated_text
        ia_rating = None

        # Intenta parsear la calificación de la última línea
        lines = generated_text.splitlines()
        if lines:
            last_line = lines[-1].strip()
            if last_line.lower().startswith('calificación:'):
                try:
                    rating_str = last_line.split(':', 1)[1].strip()
                    ia_rating = float(rating_str)
                    # Elimina la línea de calificación de la reseña final
                    ia_review = "\n".join(lines[:-1]).strip()
                except ValueError:
                    print(f"Advertencia: No se pudo parsear la calificación de '{last_line}'.")
                    ia_rating = None
            else:
                print(f"Advertencia: La última línea no contenía 'Calificación:'. Recibido: '{last_line}'")
                ia_rating = None

        # Fallback si la calificación no se pudo extraer o es inválida
        if ia_rating is None or not (1 <= ia_rating <= 5):
            print("Asignando calificación por defecto debido a error en la extracción o valor fuera de rango.")
            ia_rating = 3.5 # Un valor por defecto razonable

        return ia_review, ia_rating

    except Exception as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        # En caso de error (ej., problema de red, API Key inválida, límite excedido),
        # devuelve un mensaje de error y una calificación por defecto.
        return (
            "No fue posible generar una reseña avanzada para esta propiedad en este momento. "
            "Disculpe las molestias. Se usó una descripción básica.",
            3.0 # Calificación por defecto en caso de fallo total
        )

# Aquí comienza el código original para ejecutar el script
if __name__ == '__main__':
    print("Este script no debe ejecutarse directamente, sino a través de update_ia_reviews.py")
    # Para pruebas directas de la función, podrías añadir algo como:
    # test_data = {
    #     'titulo': 'Hermosa Villa con Piscina',
    #     'descripcion': 'Lujosa villa con amplios jardines y acabados de primera.',
    #     'ciudad': 'Guayaquil',
    #     'tipo_propiedad': 'Casa',
    #     'num_habitaciones': 4,
    #     'num_banos': 3,
    #     'metros_cuadrados': 300,
    #     'tiene_garaje': True,
    #     'caracteristicas_adicionales': 'Piscina, área de BBQ, seguridad 24/7.'
    # }
    # review, rating = generate_ia_review_and_rating(test_data)
    # print(f"\nReseña generada:\n{review}\nCalificación: {rating}")
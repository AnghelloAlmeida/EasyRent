import os
import sys
import django
from django.conf import settings
from dotenv import load_dotenv

# Obtener la ruta del directorio del script
script_dir = os.path.dirname(__file__)

# Obtener la ruta del directorio raíz del proyecto (el padre del directorio 'scripts')
# Si ai_generator.py está en 'propiedades/ai_generator.py' y .env está en la raíz del proyecto,
# entonces project_root sería el nivel de 'manage.py'.
# Ajusta '..' según la estructura real de tu proyecto.
# Si 'ai_generator.py' está en 'propiedades/', entonces 'propiedades/../..' te lleva a la raíz del proyecto.
project_root = os.path.abspath(os.path.join(script_dir, '..', '..')) # Asumiendo que propiedades/ está al mismo nivel que manage.py

# Añadir la ruta raíz del proyecto al sys.path para que Django pueda encontrar los settings
sys.path.append(project_root)

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrent_demo.settings')
django.setup()

# Importar el SDK de Google Generative AI
import google.generativeai as genai

# --- Carga y Configuración de la API de Gemini ---
# La variable de entorno GOOGLE_API_KEY debe estar cargada antes de genai.configure.
# Aquí la cargamos directamente de .env en la raíz del proyecto para este script específico.
load_dotenv(os.path.join(project_root, '.env')) # Carga el .env desde la raíz del proyecto

API_KEY = os.getenv('GOOGLE_API_KEY') # Obtener la clave del entorno

if not API_KEY:
    # Registra un error y lanza una excepción si la clave no se encuentra
    raise ValueError("La variable de entorno 'GOOGLE_API_KEY' no está configurada. "
                     "Asegúrate de tenerla en tu archivo .env en la raíz de easyrent_demo.")

genai.configure(api_key=API_KEY)
# --- FIN Carga y Configuración de la API de Gemini ---

# A PARTIR DE AQUÍ TU CÓDIGO ORIGINAL, CON LA LÓGICA DE IA DE GEMINI INTEGRADA
# (No necesitas importar Propiedad si este script solo genera la reseña y no interactúa con la DB directamente)
# from propiedades.models import Propiedad # Comentada si no se usa directamente aquí

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
        # --- CORRECCIÓN CLAVE: CAMBIO DE MODELO ---
        # El error 404 indica que 'gemini-pro' no está disponible o no soporta generateContent en tu región/configuración.
        # Intentaremos con 'gemini-1.5-flash' que es más reciente y generalmente disponible para esta tarea.
        # Si 'gemini-1.5-flash' también falla, prueba con 'gemini-1.0-pro'.
        model = genai.GenerativeModel('gemini-1.5-flash') # <-- AQUÍ ESTÁ EL CAMBIO IMPORTANTE
        # --- FIN CORRECCIÓN CLAVE ---

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
                    # Asegúrate de que la calificación esté en el rango 1-5
                    ia_rating = max(1.0, min(5.0, ia_rating))
                    # Elimina la línea de calificación de la reseña final
                    ia_review = "\n".join(lines[:-1]).strip()
                except ValueError:
                    print(f"Advertencia: No se pudo parsear la calificación de '{last_line}'. Valor por defecto (3.0) asignado.")
                    ia_rating = None
            else:
                print(f"Advertencia: La última línea de la respuesta de IA no contenía 'Calificación:'. Recibido: '{last_line}'. Valor por defecto (3.0) asignado.")
                ia_rating = None

        # Fallback si la calificación no se pudo extraer o es inválida
        if ia_rating is None: # Simplificado para cubrir todos los casos donde ia_rating no es numérico válido
            ia_rating = 3.0 # Un valor por defecto razonable si no se pudo extraer

        return ia_review, ia_rating

    except Exception as e:
        # Registrar el error completo para depuración
        print(f"Error al llamar a la API de Gemini: {e}")
        # En caso de error, devuelve un mensaje de error y una calificación por defecto.
        # El mensaje de error aquí es para el log del script; el mensaje al usuario se maneja en views.py
        return (
            "No fue posible generar una reseña avanzada para esta propiedad en este momento. "
            "Disculpe las molestias. Se usó una descripción básica.",
            3.0
        )

# Aquí comienza el código original para ejecutar el script
if __name__ == '__main__':
    print("Este script no debe ejecutarse directamente, sino a través de su importación.")
    print("Para probar la función generate_ia_review_and_rating, descomenta las líneas de prueba.")

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
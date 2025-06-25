# propiedades/ai_generator.py

import os
import sys
import django
from django.conf import settings
from dotenv import load_dotenv
import google.generativeai as genai
import google.api_core.exceptions

# Obtener la ruta del directorio del script
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrent_demo.settings')
django.setup()

load_dotenv(os.path.join(project_root, '.env'))
API_KEY = os.getenv('GOOGLE_API_KEY')

if not API_KEY:
    raise ValueError("La variable de entorno 'GOOGLE_API_KEY' no está configurada. "
                     "Asegúrate de tenerla en tu archivo .env en la raíz de easyrent_demo.")

genai.configure(api_key=API_KEY)

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

    prompt = f"""Genera una reseña objetiva (90-150 palabras) de una propiedad inmobiliaria en español, destacando sus características y su atractivo en {ciudad}. Menciona el tipo de propiedad, habitaciones, baños, si tiene garaje y características adicionales. La reseña debe reflejar la calidad real de la propiedad.

    Al final, en una LÍNEA NUEVA, proporciona una calificación numérica realista del 1 al 5 (puedes usar decimales como 4.5), usando el prefijo 'Calificación:'.

    **Criterios de Calificación Realista:**
    - **5.0 (Lujo/Excepcional):** Propiedades con alto número de habitaciones (8+), muchos baños (5+), amplios metros cuadrados (400m²+), y/o características de lujo como piscinas, jardines extensos, vistas panorámicas, áreas de entretenimiento especializadas (cine, gimnasio).
    - **4.0-4.9 (Muy Buena/Superior):** Propiedades que superan las expectativas promedio en tamaño, comodidades (ej. 4-7 hab, 3-4 baños, 150-399m², algunas características adicionales), o ubicación.
    - **3.0-3.9 (Buena/Estándar):** Propiedades que cumplen bien las necesidades básicas (ej. 2-3 hab, 1-2 baños, 50-149m², funcional).
    - **2.0-2.9 (Aceptable/Básica):** Propiedades con algunas limitaciones, o muy sencillas (ej. 1 hab, 1 baño, <50m²).
    - **1.0-1.9 (Baja/Requiere mejoras):** Propiedades con deficiencias importantes o muy pocas comodidades.

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
Caracteristicas Adicionales: {caracteristicas_adicionales if caracteristicas_adicionales else 'Ninguna.'}
---
Ejemplo de Salida para propiedad de 2 habitaciones, 1 baño, sin lujos:
Esta cómoda propiedad en {ciudad} es ideal para solteros o parejas. Con 2 habitaciones y 1 baño, ofrece un espacio funcional y bien distribuido...
Calificación: 3.2
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Modelo que te funciona rápido
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.0}, # Temperatura baja para consistencia
            request_options={"timeout": 60} # Timeout para evitar cuelgues
        )
        generated_text = response.text.strip()

        ia_review = generated_text
        ia_rating = None

        lines = generated_text.splitlines()
        if lines:
            last_line = lines[-1].strip()
            if last_line.lower().startswith('calificación:'):
                try:
                    rating_str = last_line.split(':', 1)[1].strip()
                    ia_rating = float(rating_str)
                    ia_rating = max(1.0, min(5.0, ia_rating))
                    ia_review = "\n".join(lines[:-1]).strip()
                except ValueError:
                    print(f"Advertencia: No se pudo parsear la calificación de '{last_line}'. Valor por defecto (3.0) asignado.")
                    ia_rating = None
            else:
                print(f"Advertencia: La última línea de la respuesta de IA no contenía 'Calificación:'. Recibido: '{last_line}'. Valor por defecto (3.0) asignado.")
                ia_rating = None

        if ia_rating is None:
            ia_rating = 3.0

        return ia_review, ia_rating

    except Exception as e:
        print(f"****************************************************")
        print(f"ERROR DETECTADO AL GENERAR RESEÑA CON GEMINI:")
        print(f"Tipo de Error: {type(e).__name__}")
        print(f"Mensaje del Error: {e}")
        print(f"Prompt enviado (PARCIAL): {prompt[:500]}...")
        print(f"****************************************************")
        return (
            "No fue posible generar una reseña avanzada para esta propiedad en este momento. "
            "Disculpe las molestias. Se usó una descripción básica.",
            3.0
        )

if __name__ == '__main__':
    print("Este script no debe ejecutarse directamente, sino a través de su importación.")
    print("Para probar la función generate_ia_review_and_rating, descomenta las líneas de prueba.")
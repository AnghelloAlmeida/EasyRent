# easyrent_demo/scripts/update_ia_reviews.py

import os
import sys
import django
from django.conf import settings

# Obtener la ruta del directorio del script
script_dir = os.path.dirname(__file__)
# Obtener la ruta del directorio raíz del proyecto (el padre del directorio 'scripts')
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Añadir la ruta raíz del proyecto al sys.path para que Django pueda encontrar los settings
sys.path.append(project_root)

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrent_demo.settings')
django.setup()

from propiedades.models import Propiedad
from propiedades.ai_generator import generate_ia_review_and_rating

def run():
    print("Iniciando la generación de reseñas IA para todas las propiedades existentes...")

    propiedades_actualizadas = 0
    for propiedad in Propiedad.objects.all():
        # Solo genera si no tiene una reseña o si quieres regenerarlas todas
        if not propiedad.ia_reseña_generada or propiedad.ia_calificacion is None:
            print(f"Generando reseña para: {propiedad.titulo} (ID: {propiedad.id})...")
            property_data = {
                'titulo': propiedad.titulo,
                'descripcion': propiedad.descripcion,
                'ciudad': propiedad.ciudad,
                'tipo_propiedad': propiedad.get_tipo_propiedad_display(),
                'num_habitaciones': propiedad.num_habitaciones,
                'num_banos': propiedad.num_banos,
                'metros_cuadrados': propiedad.metros_cuadrados,
                'tiene_garaje': propiedad.tiene_garaje,
                'caracteristicas_adicionales': propiedad.caracteristicas_adicionales,
            }
            try:
                ia_review, ia_rating = generate_ia_review_and_rating(property_data)
                propiedad.ia_reseña_generada = ia_review
                propiedad.ia_calificacion = ia_rating
                propiedad.save()
                propiedades_actualizadas += 1
                print(f"Reseña generada y guardada para {propiedad.titulo}.")
            except Exception as e:
                print(f"Error al generar reseña para {propiedad.titulo}: {e}")
        else:
            print(f"La propiedad {propiedad.titulo} (ID: {propiedad.id}) ya tiene reseña IA. Saltando.")

    print(f"\nProceso completado. Se actualizaron {propiedades_actualizadas} propiedades.")

if __name__ == '__main__':
    run()
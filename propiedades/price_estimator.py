# propiedades/price_estimator.py

def estimate_price(data):
    """
    Simula la estimación de precio de una propiedad basada en sus características.
    Este es un modelo dummy. En un entorno real, se usaría un modelo de ML entrenado.

    Args:
        data (dict): Un diccionario con las características de la propiedad.
                     Ej: {
                         'metros_cuadrados': 150,
                         'num_habitaciones': 3,
                         'num_banos': 2,
                         'ciudad': 'Quito',
                         'tipo_propiedad': 'casa',
                         'tiene_garaje': True,
                         'caracteristicas_adicionales': 'piscina,jardin'
                     }

    Returns:
        float: El precio estimado de la propiedad.
    """
    base_price = 50000.0  # Precio base inicial

    # Ajustes por metros cuadrados (ej: $1000 por m²)
    if data.get('metros_cuadrados'):
        base_price += float(data['metros_cuadrados']) * 1000

    # Ajustes por número de habitaciones (ej: $10000 por habitación)
    if data.get('num_habitaciones'):
        base_price += int(data['num_habitaciones']) * 10000

    # Ajustes por número de baños (ej: $5000 por baño)
    if data.get('num_banos'):
        base_price += int(data['num_banos']) * 5000

    # Ajustes por tipo de propiedad
    tipo = data.get('tipo_propiedad')
    if tipo == 'casa':
        base_price += 20000
    elif tipo == 'apartamento':
        base_price += 10000
    elif tipo == 'villa':
        base_price += 50000
    elif tipo == 'local_comercial':
        base_price += 30000
    elif tipo == 'oficina':
        base_price += 15000
    elif tipo == 'terreno':
        base_price -= 5000 # Los terrenos pueden ser más baratos por no tener construcción inicial
    elif tipo == 'bodega':
        base_price += 25000

    # Ajustes por tener garaje
    if data.get('tiene_garaje'):
        base_price += 8000

    # Ajustes por ciudad (ej: algunas ciudades son más caras)
    ciudad = data.get('ciudad', '').lower()
    if 'guayaquil' in ciudad:
        base_price += 30000
    elif 'quito' in ciudad:
        base_price += 40000
    elif 'cuenca' in ciudad:
        base_price += 20000
    # Añade más ciudades y sus ajustes si lo deseas

    # Ajustes por características adicionales (simple búsqueda de palabras clave)
    caracteristicas = data.get('caracteristicas_adicionales', '').lower()
    if 'piscina' in caracteristicas:
        base_price += 15000
    if 'jardin' in caracteristicas:
        base_price += 7000
    if 'balcon' in caracteristicas:
        base_price += 3000
    if 'seguridad' in caracteristicas:
        base_price += 5000
    if 'amueblado' in caracteristicas:
        base_price += 10000
    if 'vista al mar' in caracteristicas:
        base_price += 25000

    # Asegurarse de que el precio no sea negativo (aunque con estos ajustes es poco probable)
    return max(1000.0, round(base_price, 2))
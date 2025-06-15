# propiedades/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

from .models import Propiedad, TIPO_PROPIEDAD_CHOICES, Profile
from .forms import PropiedadForm, UserRegisterForm, UserProfileForm, ProfileUpdateForm
from .price_estimator import estimate_price
from .ai_generator import generate_ia_review_and_rating # <--- NUEVA IMPORTACIÓN


# --- Función Auxiliar para Filtrar Propiedades ---
def get_filtered_properties(request):
    """
    Aplica filtros de búsqueda a las propiedades y devuelve el QuerySet filtrado
    junto con un diccionario de los parámetros de filtro actuales.
    """
    propiedades = Propiedad.objects.filter(disponible=True).order_by('-fecha_publicacion')

    # Obtener parámetros de la URL para filtrado
    query = request.GET.get('buscar')
    ciudad = request.GET.get('ciudad')
    min_habitaciones = request.GET.get('habitaciones')
    min_banos = request.GET.get('banos')
    min_metros_cuadrados = request.GET.get('metros_cuadrados_min')
    max_metros_cuadrados = request.GET.get('metros_cuadrados_max')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    tipo_propiedad = request.GET.get('tipo_propiedad')
    tiene_garaje = request.GET.get('tiene_garaje')
    caracteristicas = request.GET.get('caracteristicas')

    # Aplicar filtros
    if query:
        propiedades = propiedades.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(ciudad__icontains=query)
        )
    if ciudad:
        propiedades = propiedades.filter(ciudad__iexact=ciudad)

    if min_habitaciones:
        try:
            min_habitaciones = int(min_habitaciones)
            propiedades = propiedades.filter(num_habitaciones__gte=min_habitaciones)
        except ValueError:
            pass # Pasa silenciosamente si hay un error de conversión (útil para AJAX)

    if min_banos:
        try:
            min_banos = int(min_banos)
            propiedades = propiedades.filter(num_banos__gte=min_banos)
        except ValueError:
            pass

    if min_metros_cuadrados:
        try:
            min_metros_cuadrados = float(min_metros_cuadrados)
            propiedades = propiedades.filter(metros_cuadrados__gte=min_metros_cuadrados)
        except ValueError:
            pass

    if max_metros_cuadrados:
        try:
            max_metros_cuadrados = float(max_metros_cuadrados)
            propiedades = propiedades.filter(metros_cuadrados__lte=max_metros_cuadrados)
        except ValueError:
            pass

    if precio_min:
        try:
            precio_min = float(precio_min)
            propiedades = propiedades.filter(precio__gte=precio_min)
        except ValueError:
            pass
    if precio_max:
        try:
            precio_max = float(precio_max)
            propiedades = propiedades.filter(precio__lte=precio_max)
        except ValueError:
            pass
    if tipo_propiedad and tipo_propiedad != '':
        propiedades = propiedades.filter(tipo_propiedad=tipo_propiedad)

    if tiene_garaje == 'on':
        propiedades = propiedades.filter(tiene_garaje=True)
    elif tiene_garaje == 'off':
        propiedades = propiedades.filter(tiene_garaje=False)

    if caracteristicas:
        propiedades = propiedades.filter(caracteristicas_adicionales__icontains=caracteristicas)

    # Devolver el QuerySet filtrado y los parámetros de filtro actuales
    return propiedades, {
        'current_query': query if query else '',
        'current_ciudad': ciudad if ciudad else '',
        'current_min_habitaciones': min_habitaciones if min_habitaciones else '',
        'current_min_banos': min_banos if min_banos else '',
        'current_min_metros_cuadrados': min_metros_cuadrados if min_metros_cuadrados else '',
        'current_max_metros_cuadrados': max_metros_cuadrados if max_metros_cuadrados else '',
        'current_precio_min': precio_min if precio_min else '',
        'current_precio_max': precio_max if precio_max else '',
        'current_tipo_propiedad': tipo_propiedad if tipo_propiedad else '',
        'current_tiene_garaje': tiene_garaje,
        'current_caracteristicas': caracteristicas,
    }


# Vista para la página de bienvenida (homepage)
def welcome_page(request):
    return render(request, 'propiedades/welcome_page.html')

# Vista para la lista de propiedades con búsqueda y filtrado (USA LA FUNCIÓN AUXILIAR)
def lista_propiedades_frontend(request):
    propiedades, current_filters = get_filtered_properties(request)

    context = {
        'propiedades': propiedades,
        'ciudades_disponibles': Propiedad.objects.values_list('ciudad', flat=True).distinct().order_by('ciudad'),
        'tipos_propiedad_choices': TIPO_PROPIEDAD_CHOICES,
        **current_filters,  # Desempaqueta el diccionario de filtros actuales
    }
    return render(request, 'propiedades/lista_propiedades.html', context)


# Vista para peticiones AJAX (USA LA FUNCIÓN AUXILIAR)
def lista_propiedades_ajax(request):
    propiedades, _ = get_filtered_properties(request) # No necesitamos los current_filters para el parcial

    context = {
        'propiedades': propiedades,
        'tipos_propiedad_choices': TIPO_PROPIEDAD_CHOICES, # Puede que no sea necesario en el parcial
    }

    html_propiedades = render_to_string('propiedades/_propiedades_list_partial.html', context, request=request)
    return HttpResponse(html_propiedades)


# Vista para el detalle de una propiedad específica
def detalle_propiedad_frontend(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    context = {
        'propiedad': propiedad
    }
    return render(request, 'propiedades/detalle_propiedad.html', context)

# Vista para la lista de propiedades del usuario logueado
@login_required
def mis_propiedades_frontend(request):
    mis_propiedades = Propiedad.objects.filter(propietario=request.user).order_by('-fecha_publicacion')
    context = {
        'propiedades': mis_propiedades
    }
    return render(request, 'propiedades/mis_propiedades.html', context)

# Vista para agregar una nueva propiedad
@login_required
def agregar_propiedad_frontend(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.propietario = request.user

            # Recopilar datos para la IA
            property_data = {
                'titulo': propiedad.titulo,
                'descripcion': propiedad.descripcion,
                'ciudad': propiedad.ciudad,
                'tipo_propiedad': propiedad.get_tipo_propiedad_display(), # Usa get_FOO_display() para el valor legible
                'num_habitaciones': propiedad.num_habitaciones,
                'num_banos': propiedad.num_banos,
                'metros_cuadrados': propiedad.metros_cuadrados,
                'tiene_garaje': propiedad.tiene_garaje,
                'caracteristicas_adicionales': propiedad.caracteristicas_adicionales,
            }

            # Generar reseña y calificación con la IA
            ia_review, ia_rating = generate_ia_review_and_rating(property_data)
            propiedad.ia_reseña_generada = ia_review
            propiedad.ia_calificacion = ia_rating

            propiedad.save() # Guarda la propiedad con los datos de la IA
            messages.success(request, '¡Propiedad agregada exitosamente y reseña IA generada!')
            return redirect('mis_propiedades_frontend')
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/agregar_propiedad.html', {'form': form})

# Vista para editar una propiedad existente
@login_required
def editar_propiedad_frontend(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            propiedad = form.save(commit=False) # No guardar aún

            # Recopilar datos para la IA (con los datos actualizados del formulario)
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

            # Generar reseña y calificación con la IA (se regenera con cada edición)
            ia_review, ia_rating = generate_ia_review_and_rating(property_data)
            propiedad.ia_reseña_generada = ia_review
            propiedad.ia_calificacion = ia_rating

            propiedad.save() # Guarda la propiedad con los datos de la IA actualizados
            messages.success(request, '¡Propiedad actualizada exitosamente y reseña IA regenerada!')
            return redirect('detalle_propiedad_frontend', pk=propiedad.pk)
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'propiedades/editar_propiedad.html', {'form': form, 'propiedad': propiedad})

# Vista para eliminar una propiedad
@login_required
def eliminar_propiedad_frontend(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk, propietario=request.user)
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, '¡Propiedad eliminada exitosamente!')
        return redirect('mis_propiedades_frontend')
    return render(request, 'propiedades/eliminar_propiedad.html', {'propiedad': propiedad})

# Vista de registro de usuario (basada en clase)
class SignUpView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
        return super().form_valid(form)

# Vista: Dashboard del usuario
@login_required
def user_dashboard_view(request):
    num_mis_propiedades = request.user.propiedad_set.count()
    context = {
        'num_mis_propiedades': num_mis_propiedades,
    }
    return render(request, 'propiedades/user_dashboard.html', context)


# VISTA ACTUALIZADA: Editar Perfil del Usuario (con formularios para User y Profile)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserProfileForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Hubo un error al actualizar tu perfil. Por favor, revisa los campos.')
    else:
        u_form = UserProfileForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'propiedades/edit_profile.html', context)


# Nueva vista para estimación de precios con IA
def estimar_precio_propiedad(request):
    if request.method == 'POST':
        # Obtener los datos del formulario que vienen por AJAX
        try:
            metros_cuadrados = float(request.POST.get('metros_cuadrados', 0))
            num_habitaciones = int(request.POST.get('num_habitaciones', 0))
            num_banos = int(request.POST.get('num_banos', 0))
            ciudad = request.POST.get('ciudad', '')
            tipo_propiedad = request.POST.get('tipo_propiedad', '')
            # Asegúrate de que el checkbox se interprete correctamente.
            # 'on' es el valor por defecto si está marcado, si no está presente, es False.
            tiene_garaje = request.POST.get('tiene_garaje') == 'on'
            caracteristicas_adicionales = request.POST.get('caracteristicas_adicionales', '')

            property_data = {
                'metros_cuadrados': metros_cuadrados,
                'num_habitaciones': num_habitaciones,
                'num_banos': num_banos,
                'ciudad': ciudad,
                'tipo_propiedad': tipo_propiedad,
                'tiene_garaje': tiene_garaje,
                'caracteristicas_adicionales': caracteristicas_adicionales
            }

            # Llamar a la función de estimación (nuestro "modelo de IA")
            estimated_price = estimate_price(property_data)

            # Devolver el precio estimado como JSON
            return JsonResponse({'estimated_price': estimated_price})
        except (ValueError, TypeError) as e:
            # Capturar errores de conversión de tipo
            return JsonResponse({'error': f'Datos de entrada inválidos: {e}'}, status=400)
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return JsonResponse({'error': f'Error interno del servidor: {e}'}, status=500)
    else:
        # Renderizar la página con el formulario para la estimación si es una petición GET
        ciudades_disponibles = Propiedad.objects.values_list('ciudad', flat=True).distinct().order_by('ciudad')
        context = {
            'tipos_propiedad_choices': TIPO_PROPIEDAD_CHOICES,
            'ciudades_disponibles': ciudades_disponibles,
        }
        return render(request, 'propiedades/estimar_precio.html', context)
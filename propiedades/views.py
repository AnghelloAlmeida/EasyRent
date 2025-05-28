from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import CreateView
# from django.contrib.auth.forms import UserCreationForm # No es necesario si usas UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Propiedad, TIPO_PROPIEDAD_CHOICES
from .forms import PropiedadForm, UserRegisterForm # Asegúrate de que UserRegisterForm está bien importado

# Vista para la página de bienvenida (homepage)
def welcome_page(request):
    return render(request, 'propiedades/welcome_page.html')

# Vista para la lista de propiedades con búsqueda y filtrado
def lista_propiedades_frontend(request):
    propiedades = Propiedad.objects.filter(disponible=True).order_by('-fecha_publicacion')

    # Obtener parámetros de la URL para filtrado
    query = request.GET.get('q') # Búsqueda por texto (título, descripción, dirección, ciudad)
    ciudad = request.GET.get('ciudad')
    min_habitaciones = request.GET.get('min_habitaciones')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    tipo_propiedad = request.GET.get('tipo_propiedad')

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
            messages.error(request, "El número mínimo de habitaciones debe ser un número entero.")
    if precio_min:
        try:
            precio_min = float(precio_min)
            propiedades = propiedades.filter(precio__gte=precio_min)
        except ValueError:
            messages.error(request, "El precio mínimo debe ser un número válido.")
    if precio_max:
        try:
            precio_max = float(precio_max)
            propiedades = propiedades.filter(precio__lte=precio_max)
        except ValueError:
            messages.error(request, "El precio máximo debe ser un número válido.")
    if tipo_propiedad and tipo_propiedad != '':
        propiedades = propiedades.filter(tipo_propiedad=tipo_propiedad)

    context = {
        'propiedades': propiedades,
        # Obtener ciudades únicas y ordenadas de las propiedades existentes
        'ciudades_disponibles': Propiedad.objects.values_list('ciudad', flat=True).distinct().order_by('ciudad'),
        'tipos_propiedad_choices': TIPO_PROPIEDAD_CHOICES,
        # Pasar los valores actuales de los filtros para mantenerlos en el formulario
        'current_query': query if query else '',
        'current_ciudad': ciudad if ciudad else '',
        'current_min_habitaciones': min_habitaciones if min_habitaciones else '',
        'current_precio_min': precio_min if precio_min else '',
        'current_precio_max': precio_max if precio_max else '',
        'current_tipo_propiedad': tipo_propiedad if tipo_propiedad else '',
    }
    return render(request, 'propiedades/lista_propiedades.html', context)

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
            propiedad.save()
            messages.success(request, '¡Propiedad agregada exitosamente!')
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
            form.save()
            messages.success(request, '¡Propiedad actualizada exitosamente!')
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
    form_class = UserRegisterForm # Usamos UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
        return super().form_valid(form)

# NUEVA VISTA: Dashboard del usuario
@login_required
def user_dashboard_view(request):
    num_mis_propiedades = request.user.propiedad_set.count()
    context = {
        'num_mis_propiedades': num_mis_propiedades,
    }
    return render(request, 'propiedades/user_dashboard.html', context)
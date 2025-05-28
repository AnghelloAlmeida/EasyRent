from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, url_name, css_class='active'):
    """
    Devuelve la clase CSS si la URL actual coincide con el nombre de URL dado.
    Útil para resaltar elementos de navegación activos.
    """
    request = context['request']
    try:
        pattern = reverse(url_name)
    except NoReverseMatch:
        # En caso de que la URL no exista, simplemente no aplica la clase
        return ''

    # Ajuste para manejar URLs que empiezan con el patrón pero no son la exacta
    # Por ejemplo, /propiedades/pk/edit debería activar 'propiedades', no 'welcome_page'
    # Esta lógica es crucial para la activación de la navegación
    if url_name == 'welcome_page':
        # welcome_page solo se activa si la ruta es exactamente '/'
        if request.path == reverse('welcome_page'):
            return css_class
        else:
            return ''
    elif url_name == 'user_dashboard':
        # user_dashboard solo se activa si la ruta es exactamente '/dashboard/'
        if request.path == reverse('user_dashboard'):
            return css_class
        else:
            return ''
    elif url_name == 'login' or url_name == 'register':
        # login/register solo se activan en su URL exacta
        if request.path == pattern:
            return css_class
        else:
            return ''
    elif request.path.startswith(pattern):
        return css_class
    return ''
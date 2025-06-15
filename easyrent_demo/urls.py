# easyrent_demo/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('propiedades.urls')),  # <-- ¡Esta línea es crucial!
]

# Para servir archivos estáticos y de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Nota: STATIC_ROOT es más para producción con collectstatic.
# En desarrollo, STATICFILES_DIRS es lo que se usa para STATIC_URL.
# Asegúrate de que tus archivos estáticos (CSS, JS) estén en propiedades/static/propiedades/

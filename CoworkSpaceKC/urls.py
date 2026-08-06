"""
URL configuration for CoworkSpaceKC project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse
import os

# Vista para servir el Service Worker con el Content-Type correcto
def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    with open(sw_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/javascript')

# Vista para servir el manifest con el Content-Type correcto
def manifest(request):
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/manifest+json')

urlpatterns = [
    # Admin de Django deshabilitado - usar el sistema de gestión web
    # path('admin/', admin.site.urls),
    
    # PWA - Service Worker y Manifest
    path('sw.js', service_worker, name='service_worker'),
    path('manifest.json', manifest, name='manifest'),
    
    # Rutas principales
    path('', include('reservas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


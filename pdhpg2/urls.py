from django.contrib import admin
from django.urls import path, include
from usuarios.views import login_view, logout_view, vista_administrador, vista_auxiliar, vista_secretaria

# Importar las vistas desde la aplicación resoluciones
from resoluciones import views as resoluciones_views

# Importar settings y static para servir archivos de medios en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta al panel de administración de Django
    path('login/', login_view, name='login'),  # Ruta para el login
    path('logout/', logout_view, name='logout'),  # Ruta para el logout

    # Rutas protegidas por roles
    path('admin-view/', vista_administrador, name='vista_administrador'),  # Ruta para la vista del administrador
    path('auxiliar-view/', vista_auxiliar, name='vista_auxiliar'),  # Ruta para la vista del auxiliar
    path('secretaria-view/', vista_secretaria, name='vista_secretaria'),  # Ruta para la vista de la secretaria
    
    # Redirección a la vista de login si el usuario no está autenticado
    path('', login_view, name='home'),

    # Incluye las URLs de la app resoluciones para manejar CRUD después del login
    path('resoluciones/', include('resoluciones.urls')),  
]

# Añadir configuración para servir archivos de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

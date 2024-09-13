from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views  # Importar las vistas de la aplicación usuarios
from resoluciones import views as resoluciones_views  # Importar las vistas desde la aplicación resoluciones
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Ruta al panel de administración de Django
    path('admin/', admin.site.urls),

    # Autenticación
    path('login/', usuarios_views.login_view, name='login'),  # Ruta para el login
    path('logout/', usuarios_views.logout_view, name='logout'),  # Ruta para el logout

    # Vistas protegidas por roles
    path('admin-view/', usuarios_views.vista_administrador, name='vista_administrador'),  # Vista de administrador
    path('auxiliar-view/', usuarios_views.vista_auxiliar, name='vista_auxiliar'),  # Vista de auxiliar
    path('secretaria-view/', usuarios_views.vista_secretaria, name='vista_secretaria'),  # Vista de secretaria

    # Redirección a la vista de login si el usuario no está autenticado
    path('', usuarios_views.login_view, name='home'),

    # Rutas para CRUD de resoluciones
    path('resoluciones/', include('resoluciones.urls')),  

    # Rutas para CRUD de usuarios (crear, editar, listar y eliminar usuarios)
    path('crear-usuario/', usuarios_views.crear_usuario, name='crear_usuario'),  # Ruta para crear usuarios
    path('editar-usuario/<int:user_id>/', usuarios_views.editar_usuario, name='editar_usuario'),  # Ruta para editar usuarios
    path('lista-usuarios/', usuarios_views.lista_usuarios, name='lista_usuarios'),  # Ruta para listar usuarios
    path('eliminar-usuario/<int:user_id>/', usuarios_views.eliminar_usuario, name='eliminar_usuario'),  # Ruta para eliminar usuarios

    # Nueva ruta para editar perfil
    path('editar-perfil/', usuarios_views.editar_perfil, name='editar_perfil'),  # Ruta para editar perfil actual
]

# Añadir configuración para servir archivos de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

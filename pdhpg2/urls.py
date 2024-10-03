from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views  # Importar las vistas de la aplicación usuarios
from resoluciones import views as resoluciones_views  # Importar las vistas desde la aplicación resoluciones
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from usuarios.views import enviar_correo_prueba, SendEmailView  # Corregir la importación aquí

urlpatterns = [
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),
    path('accounts/', include('allauth.urls')),
    # Ruta al panel de administración de Django
    path('admin/', admin.site.urls),
    path('enviar-correo/', enviar_correo_prueba),  # Añadir esta línea
    path('send-email/', SendEmailView.as_view(), name='send_email'),

    # Autenticación
    path('login/', usuarios_views.login_view, name='login'),  # Ruta para el login
    path('logout/', usuarios_views.logout_view, name='logout'),  # Ruta para el logout
    # Rutas para la funcionalidad de restablecimiento de contraseña
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),

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

    # Rutas para generar reportes PDF y Excel de resoluciones
    path('resoluciones/reporte/pdf/', resoluciones_views.generar_reporte_pdf, name='generar_reporte_pdf'),  # Ruta para generar PDF
    path('resoluciones/reporte/excel/', resoluciones_views.generar_reporte_excel, name='generar_reporte_excel'),  # Ruta para generar Excel
]

# Añadir configuración para servir archivos de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

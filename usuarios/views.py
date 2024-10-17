from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group  # Aquí se importa Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from resoluciones.models import ResolucionFinal
from usuarios.forms import CustomUserCreationForm, UserEditForm
from resoluciones.forms import ResolucionForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.views import View
from django.shortcuts import render

# Funciones de verificación de roles
def es_administrador(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

def es_auxiliar(user):
    return user.groups.filter(name='Auxiliar').exists()

def es_secretaria(user):
    return user.groups.filter(name='Secretaria').exists()

def es_policia(user):
    return user.groups.filter(name='policia').exists()

# Vista de login
# Vista de login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige a todos los roles al dashboard
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciales incorrectas.')
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


# Función para cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda user: es_administrador(user) or es_auxiliar(user) or es_policia(user) or user.is_superuser)
def crear_resolucion(request):
    if request.method == 'POST':
        form = ResolucionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_resolucion = form.save(commit=False)
            nueva_resolucion.creado_por = request.user  # Asigna el usuario que crea la resolución
            nueva_resolucion.save()
            messages.success(request, 'Resolución creada exitosamente.')
            return redirect('dashboard')  # Redirigir al dashboard después de crear
    else:
        form = ResolucionForm()
    return render(request, 'resoluciones/crear_resolucion.html', {'form': form})

# Función para crear un usuario sin restricciones de acceso
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignar rol al usuario basado en la selección
            role = request.POST.get('role')
            if role:  # Verifica si se seleccionó un rol
                group = Group.objects.get(name=role)  # Se obtiene el grupo basado en el nombre del rol
                user.groups.add(group)
            
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('login')  # Redirige al login después de crear el usuario
        else:
            # Mostrar los errores si el formulario no es válido
            print(form.errors)
            messages.error(request, 'Hubo un error al crear el usuario. Revisa los campos.')
    else:
        form = CustomUserCreationForm()

    # Seleccionar plantilla en función del estado de autenticación
    if request.user.is_authenticated:
        return render(request, 'usuarios/crear_usuario.html', {'form': form})
    else:
        return render(request, 'usuarios/crear_usuario_simple.html', {'form': form})

# Vista para listar usuarios
@login_required
@user_passes_test(es_administrador)
def lista_usuarios(request):
    usuarios = User.objects.all()
    
    # Creamos una lista para almacenar usuarios con sus roles
    usuarios_con_roles = []

    for usuario in usuarios:
        # Obtener los grupos (roles) del usuario
        grupos = usuario.groups.values_list('name', flat=True)
        roles = ', '.join(grupos) if grupos else 'Sin rol asignado'

        # Agregamos cada usuario con su rol
        usuarios_con_roles.append({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'date_joined': usuario.date_joined,
            'roles': roles,  # Agregamos los roles aquí
        })

    # Pasamos la lista de usuarios con roles al template
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios_con_roles': usuarios_con_roles})

# Vista del policía (solo puede ver y crear resoluciones)
@login_required
@user_passes_test(es_policia)
def vista_policia(request):
    query = request.GET.get('q')
    if query:
        resoluciones = ResolucionFinal.objects.filter(
            Q(expediente__icontains=query) |
            Q(denunciante__icontains=query) |
            Q(victima__icontains=query) |
            Q(derecho_humano_violado__icontains=query) |
            Q(resolucion__icontains=query) |
            Q(calificacion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(responsable__icontains=query) |
            Q(estado__icontains=query)
        )
    else:
        resoluciones = ResolucionFinal.objects.all()

    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': False, 'es_policia': True})

# Función para editar un usuario
@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

            # Limpiar los grupos actuales del usuario y asignar el nuevo rol
            usuario.groups.clear()
            role = request.POST.get('role')
            group = Group.objects.get(name=role)
            usuario.groups.add(group)

            messages.success(request, 'Usuario editado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=usuario)
    
    # Pasar el usuario al template para determinar el rol actual
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'user': usuario})

# Función para eliminar un usuario
@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})

# Vista del administrador con búsqueda por parámetro 'q'
@login_required
@user_passes_test(es_administrador)
def vista_administrador(request):
    query = request.GET.get('q')
    if query:
        resoluciones = ResolucionFinal.objects.filter(
            Q(expediente__icontains=query) |
            Q(denunciante__icontains=query) |
            Q(victima__icontains=query) |
            Q(derecho_humano_violado__icontains=query) |
            Q(resolucion__icontains=query) |
            Q(calificacion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(responsable__icontains=query) |
            Q(estado__icontains=query)
        )
    else:
        resoluciones = ResolucionFinal.objects.all()

    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': True})

# Vista del auxiliar con búsqueda por parámetro 'q'
@login_required
@user_passes_test(es_auxiliar)
def vista_auxiliar(request):
    query = request.GET.get('q')
    if query:
        resoluciones = ResolucionFinal.objects.filter(
            Q(expediente__icontains=query) |
            Q(denunciante__icontains=query) |
            Q(victima__icontains=query) |
            Q(derecho_humano_violado__icontains=query) |
            Q(resolucion__icontains=query) |
            Q(calificacion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(responsable__icontains=query) |
            Q(estado__icontains=query)
        )
    else:
        resoluciones = ResolucionFinal.objects.all()

    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': True})

# Vista de la secretaria con búsqueda por parámetro 'q'
@login_required
@user_passes_test(es_secretaria)
def vista_secretaria(request):
    query = request.GET.get('q')
    if query:
        resoluciones = ResolucionFinal.objects.filter(
            Q(expediente__icontains=query) |
            Q(denunciante__icontains=query) |
            Q(victima__icontains=query) |
            Q(derecho_humano_violado__icontains=query) |
            Q(resolucion__icontains=query) |
            Q(calificacion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(responsable__icontains=query) |
            Q(estado__icontains=query)
        )
    else:
        resoluciones = ResolucionFinal.objects.all()

    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': False})

@login_required
def editar_perfil(request):
    usuario = request.user  # Obtener el usuario actual
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('vista_administrador')
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

# Vista para enviar correo con plantilla personalizada
class SendEmailView(View):
    def get(self, request):
        return render(request, 'mail/send.html')
    
    def post(self, request):
        # Obtener el correo del formulario
        email = request.POST.get('email')
        print(f"Email capturado: {email}")

        if email:
            # Cargar el template del correo
            template = get_template('mail/email-order-success.html')

            # Renderizar el template con contenido dinámico
            content = template.render({'email': email})

            # Crear el mensaje de correo con asunto, mensaje, emisor, y receptor
            msg = EmailMultiAlternatives(
                'Gracias por tu compra',
                'Este es un correo de confirmación',
                settings.EMAIL_HOST_USER,
                [email]
            )

            # Adjuntar el contenido HTML al mensaje
            msg.attach_alternative(content, 'text/html')

            try:
                # Intentar enviar el correo
                msg.send()
                print("Correo enviado correctamente")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
        else:
            print("No se recibió ningún correo en la solicitud POST")

        return render(request, 'mail/send.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from resoluciones.models import ResolucionFinal
from usuarios.forms import CustomUserCreationForm, UserEditForm
from resoluciones.forms import ResolucionForm

# Funciones de verificación de roles
def es_administrador(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

def es_auxiliar(user):
    return user.groups.filter(name='Auxiliar').exists()

def es_secretaria(user):
    return user.groups.filter(name='Secretaria').exists()

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
                if es_administrador(user):
                    return redirect('vista_administrador')
                elif es_auxiliar(user):
                    return redirect('vista_auxiliar')
                elif es_secretaria(user):
                    return redirect('vista_secretaria')
                else:
                    return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

# Vista de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Función para crear una resolución
@login_required
@user_passes_test(es_administrador)
def crear_resolucion(request):
    if request.method == 'POST':
        form = ResolucionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_resolucion = form.save(commit=False)
            nueva_resolucion.creado_por = request.user  # Asigna el usuario que crea la resolución
            nueva_resolucion.save()
            messages.success(request, 'Resolución creada exitosamente.')
            return redirect('vista_administrador')
    else:
        form = ResolucionForm()
    return render(request, 'resoluciones/crear_resolucion.html', {'form': form})

# Función para crear un usuario
@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

# Función para editar un usuario
@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

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

# Vista para listar usuarios
@login_required
@user_passes_test(es_administrador)
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

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
            Q(resolucion__icontains=query) |  # Verifica si este campo es correcto en tu modelo
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
            Q(resolucion__icontains=query) |  # Verifica si este campo es correcto en tu modelo
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
            Q(resolucion__icontains=query) |  # Verifica si este campo es correcto en tu modelo
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
            return redirect('vista_administrador')  # Redirigir a alguna vista después de la edición
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

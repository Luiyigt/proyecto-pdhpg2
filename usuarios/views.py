from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from resoluciones.models import ResolucionFinal

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
                # Redirigir según el rol del usuario
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

# Vistas protegidas según roles
@login_required
@user_passes_test(es_administrador)
def vista_administrador(request):
    # Mostrar directamente la lista de resoluciones para administradores
    resoluciones = ResolucionFinal.objects.all()
    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': True})

@login_required
@user_passes_test(es_auxiliar)
def vista_auxiliar(request):
    # Mostrar directamente la lista de resoluciones para auxiliares
    resoluciones = ResolucionFinal.objects.all()
    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': True})

@login_required
@user_passes_test(es_secretaria)
def vista_secretaria(request):
    # Mostrar directamente la lista de resoluciones para secretarias (solo visualización)
    resoluciones = ResolucionFinal.objects.all()
    return render(request, 'resoluciones/lista_resoluciones.html', {'resoluciones': resoluciones, 'es_auxiliar_o_superusuario': False})

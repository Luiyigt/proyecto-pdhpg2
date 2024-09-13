from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q  # Importar para búsquedas complejas
from .models import ResolucionFinal
from .forms import ResolucionForm
from django.contrib import messages  # Importar para manejar los mensajes
from django.views.decorators.csrf import csrf_exempt

@login_required
def lista_resoluciones(request):
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda 'q'
    
    # Si hay un término de búsqueda, filtrar por varios campos
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
        # Si no hay término de búsqueda, mostrar todas las resoluciones
        resoluciones = ResolucionFinal.objects.all()

    es_auxiliar_o_superusuario = request.user.groups.filter(name='Auxiliar').exists() or request.user.is_superuser

    return render(request, 'resoluciones/lista_resoluciones.html', {
        'resoluciones': resoluciones,
        'es_auxiliar_o_superusuario': es_auxiliar_o_superusuario
    })

@login_required
def detalle_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    return render(request, 'resoluciones/detalle_resolucion.html', {'resolucion': resolucion})

@csrf_exempt
@login_required
@user_passes_test(lambda user: user.groups.filter(name='Auxiliar').exists() or user.is_superuser)
def crear_resolucion(request):
    if request.method == "POST":
        form = ResolucionForm(request.POST, request.FILES)
        if form.is_valid():
            resolucion = form.save(commit=False)
            resolucion.creado_por = request.user
            resolucion.save()
            messages.success(request, 'Resolución creada exitosamente.')
            return redirect('detalle_resolucion', pk=resolucion.pk)
        else:
            messages.error(request, 'Hubo un error en el formulario. Revisa los campos e intenta de nuevo.')
    else:
        form = ResolucionForm()
    return render(request, 'resoluciones/crear_resolucion.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Auxiliar').exists() or user.is_superuser)
def editar_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    if request.method == "POST":
        form = ResolucionForm(request.POST, request.FILES, instance=resolucion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resolución actualizada exitosamente.')
            return redirect('detalle_resolucion', pk=resolucion.pk)  # Asegúrate de pasar el pk correctamente
        else:
            messages.error(request, 'Hubo un error al actualizar la resolución. Revisa los campos e intenta de nuevo.')
    else:
        form = ResolucionForm(instance=resolucion)
    return render(request, 'resoluciones/editar_resolucion.html', {'form': form, 'resolucion': resolucion})

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Auxiliar').exists() or user.is_superuser)
def eliminar_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    if request.method == "POST":
        resolucion.delete()
        messages.success(request, 'Resolución eliminada exitosamente.')
        return redirect('lista_resoluciones')  # Redirigir a la lista después de eliminar
    return render(request, 'resoluciones/eliminar_resolucion.html', {'resolucion': resolucion})

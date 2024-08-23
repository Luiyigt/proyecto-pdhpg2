from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ResolucionFinal
from .forms import ResolucionForm

@login_required
def lista_resoluciones(request):
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

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Auxiliar').exists() or user.is_superuser)
def crear_resolucion(request):
    if request.method == "POST":
        form = ResolucionForm(request.POST, request.FILES)
        if form.is_valid():
            resolucion = form.save(commit=False)
            resolucion.creado_por = request.user
            resolucion.save()
            return redirect('detalle_resolucion', pk=resolucion.pk)  # Redirigir al detalle después de crear
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
            return redirect('detalle_resolucion', pk=resolucion.pk)  # Asegúrate de pasar el pk correctamente
    else:
        form = ResolucionForm(instance=resolucion)
    return render(request, 'resoluciones/editar_resolucion.html', {'form': form, 'resolucion': resolucion})

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Auxiliar').exists() or user.is_superuser)
def eliminar_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    if request.method == "POST":
        resolucion.delete()
        return redirect('lista_resoluciones')  # Redirigir a la lista después de eliminar
    return render(request, 'resoluciones/eliminar_resolucion.html', {'resolucion': resolucion})

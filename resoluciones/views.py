from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q  # Importar para búsquedas complejas
from .models import ResolucionFinal
from .forms import ResolucionForm
from django.contrib import messages  # Importar para manejar los mensajes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS  # Importar para generar PDF
import pandas as pd  # Importar para generar archivos Excel
from django.conf import settings  # Para gestionar rutas estáticas
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator  # Importar Paginator para la paginación
import datetime

# Función para verificar si el usuario es administrador o superusuario
def es_administrador_o_superusuario(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

@login_required
def lista_resoluciones(request):
    query = request.GET.get('q', '')  # Obtener el parámetro de búsqueda 'q'
    per_page = request.GET.get('per_page', 10)  # Obtener el número de resoluciones por página, por defecto 10
    
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

    # Paginación
    paginator = Paginator(resoluciones, per_page)  # Paginador con el número de resoluciones por página
    page_number = request.GET.get('page')  # Número de página actual
    page_obj = paginator.get_page(page_number)

    es_auxiliar_o_superusuario = request.user.groups.filter(name='Auxiliar').exists() or request.user.is_superuser
    es_policia = request.user.groups.filter(name='policia').exists()

    return render(request, 'resoluciones/lista_resoluciones.html', {
        'page_obj': page_obj,  # Pasar el objeto de la página
        'es_auxiliar_o_superusuario': es_auxiliar_o_superusuario,
        'es_policia': es_policia,
        'per_page': per_page,  # Pasar el número de elementos por página
    })

@login_required
def detalle_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    es_policia = request.user.groups.filter(name='policia').exists()  # Verificar si es policía
    return render(request, 'resoluciones/detalle_resolucion.html', {'resolucion': resolucion, 'es_policia': es_policia})

@csrf_exempt
@login_required
@user_passes_test(lambda user: es_administrador_o_superusuario(user) or user.groups.filter(name='Auxiliar').exists() or user.groups.filter(name='policia').exists())
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
@user_passes_test(lambda user: es_administrador_o_superusuario(user) or user.groups.filter(name='Auxiliar').exists())
def editar_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    if request.method == "POST":
        form = ResolucionForm(request.POST, request.FILES, instance=resolucion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resolución actualizada exitosamente.')
            return redirect('detalle_resolucion', pk=resolucion.pk)
        else:
            messages.error(request, 'Hubo un error al actualizar la resolución. Revisa los campos e intenta de nuevo.')
    else:
        form = ResolucionForm(instance=resolucion)
    return render(request, 'resoluciones/editar_resolucion.html', {'form': form, 'resolucion': resolucion})

@login_required
@user_passes_test(lambda user: es_administrador_o_superusuario(user) or user.groups.filter(name='Auxiliar').exists())
def eliminar_resolucion(request, pk):
    resolucion = get_object_or_404(ResolucionFinal, pk=pk)
    if request.method == "POST":
        resolucion.delete()
        messages.success(request, 'Resolución eliminada exitosamente.')
        return redirect('lista_resoluciones')  # Redirigir a la lista después de eliminar
    return render(request, 'resoluciones/eliminar_resolucion.html', {'resolucion': resolucion})

# --- NUEVAS FUNCIONALIDADES DE REPORTE PDF Y EXCEL ---

# Generación de reportes en PDF
@login_required
def generar_reporte_pdf(request):
    resoluciones = ResolucionFinal.objects.all()

    # Renderizar la plantilla del PDF
    html_string = render_to_string('resoluciones/reporte_pdf.html', {'resoluciones': resoluciones})

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_resoluciones.pdf"'

    # Obtener la ruta del archivo CSS para WeasyPrint
    css_path = settings.STATICFILES_DIRS[0] + '/css/pdf_styles.css'

    # Generar el PDF con orientación horizontal y ajustar el contenido
    HTML(string=html_string).write_pdf(response, stylesheets=[CSS(css_path)])

    return response

# Generación de reportes en Excel
@login_required
def generar_reporte_excel(request):
    resoluciones = ResolucionFinal.objects.all()

    # Crear DataFrame con los datos de las resoluciones
    data = {
        'ID': [r.id for r in resoluciones],
        'Expediente': [r.expediente for r in resoluciones],
        'Denunciante': [r.denunciante for r in resoluciones],
        'Fecha Resolución': [r.fecha_resolucion for r in resoluciones],
        'Estado': [r.estado for r in resoluciones],
    }
    df = pd.DataFrame(data)

    # Crear el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_resoluciones.xlsx"'
    df.to_excel(response, index=False)

    return response

@login_required
def lista_reportes(request):
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

    # Verificar si el usuario es auxiliar, superusuario o policía
    es_auxiliar_o_superusuario = request.user.groups.filter(name='Auxiliar').exists() or request.user.is_superuser
    es_policia = request.user.groups.filter(name='policia').exists()

    return render(request, 'reportes/lista_reportes.html', {
        'resoluciones': resoluciones,
        'es_auxiliar_o_superusuario': es_auxiliar_o_superusuario,
        'es_policia': es_policia
    })

@login_required
def dashboard_view(request):
    # Cantidad de resoluciones
    total_resoluciones = ResolucionFinal.objects.count()

    # Cantidad de usuarios
    total_usuarios = User.objects.count()

    # Cantidad de PDFs
    total_pdfs = ResolucionFinal.objects.filter(archivo_adjunto__isnull=False).count()

    # Gráfico circular de tipos de derechos humanos violados
    derechos_humanos_data = (
        ResolucionFinal.objects.values('derecho_humano_violado')
        .annotate(count=Count('derecho_humano_violado'))
    )

    derechos_labels = [data['derecho_humano_violado'] for data in derechos_humanos_data]
    derechos_values = [data['count'] for data in derechos_humanos_data]

    context = {
        'total_resoluciones': total_resoluciones,
        'total_usuarios': total_usuarios,
        'total_pdfs': total_pdfs,
        'derechos_labels': derechos_labels,
        'derechos_values': derechos_values,
    }

    return render(request, 'dashboard/dashboard.html', context)

def filtrar_grafica(request): 
    # Obtener los parámetros de año y mes
    year = request.GET.get('year')
    month = request.GET.get('month')

    # Si no se seleccionan año ni mes, devolver todas las resoluciones
    resoluciones = ResolucionFinal.objects.all()

    if year:
        resoluciones = resoluciones.filter(fecha_resolucion__year=year)
    if month:
        resoluciones = resoluciones.filter(fecha_resolucion__month=month)

    # Contar los tipos de derechos humanos violados
    derechos_violados = resoluciones.values('derecho_humano_violado').annotate(count=Count('derecho_humano_violado'))

    # Preparar los datos para la gráfica
    labels = [item['derecho_humano_violado'] for item in derechos_violados]
    values = [item['count'] for item in derechos_violados]

    # Verificar si no hay resultados, para devolver todos los datos sin filtro
    if not year and not month:
        # Si no se seleccionan filtros, devolver todas las resoluciones
        labels = resoluciones.values_list('derecho_humano_violado', flat=True).distinct()
        values = [resoluciones.filter(derecho_humano_violado=label).count() for label in labels]

    return JsonResponse({'labels': list(labels), 'values': list(values)})

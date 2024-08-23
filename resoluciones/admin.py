from django.contrib import admin
from .models import ResolucionFinal

@admin.register(ResolucionFinal)
class ResolucionFinalAdmin(admin.ModelAdmin):
    list_display = (
        'expediente', 
        'denunciante', 
        'victima', 
        'derecho_humano_violado', 
        'resolucion', 
        'calificacion', 
        'direccion', 
        'fecha_resolucion', 
        'responsable', 
        'estado', 
        'archivo_adjunto', 
        'creado_por', 
        'fecha_creacion'
    )
    search_fields = ('expediente', 'denunciante', 'victima', 'derecho_humano_violado')
    list_filter = ('estado', 'fecha_resolucion', 'creado_por')

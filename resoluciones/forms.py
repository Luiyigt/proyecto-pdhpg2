from django import forms
from .models import ResolucionFinal

class ResolucionForm(forms.ModelForm):
    class Meta:
        model = ResolucionFinal
        fields = ['expediente', 'denunciante', 'victima', 'derecho_humano_violado', 'resolucion', 'calificacion', 'direccion', 'fecha_resolucion', 'responsable', 'estado', 'archivo_adjunto']

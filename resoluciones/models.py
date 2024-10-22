from django.db import models
from django.contrib.auth.models import User

class ResolucionFinal(models.Model):
    expediente = models.CharField(max_length=50, unique=True)  # Número de expediente
    denunciante = models.CharField(max_length=255)  # Nombre del denunciante
    victima = models.CharField(max_length=255)  # Nombre de la víctima
    derecho_humano_violado = models.CharField(max_length=255)  # Descripción del derecho humano violado
    resolucion = models.TextField()  # Texto de la resolución
    calificacion = models.CharField(max_length=50)  # Calificación de la resolución
    direccion = models.CharField(max_length=255, null=True, blank=True)  # Dirección relacionada
    fecha_resolucion = models.DateField()  # Fecha de la resolución
    responsable = models.CharField(max_length=255, null=True, blank=True)  # Responsable de la violación del derecho humano
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Resuelta', 'Resuelta'), ('En Proceso', 'En Proceso')])  # Estado de la resolución
    archivo_adjunto = models.FileField(upload_to='resoluciones/', null=True, blank=True)  # Archivo adjunto
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Usuario que creó la resolución
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del registro

    def __str__(self):
        return f'Expediente {self.expediente} - {self.estado}'

    class Meta:
        verbose_name = 'Resolución Final'
        verbose_name_plural = 'Resoluciones Finales'
        ordering = ['-fecha_resolucion']
        
    @property
    def archivo_url(self):
        if self.archivo_adjunto:
            # Aquí construimos manualmente la URL con el prefijo 'resoluciones/media/'
            return f'/resoluciones/media/{self.archivo_adjunto.name}'
        return ''

    def __str__(self):
        return f'Expediente {self.expediente}'
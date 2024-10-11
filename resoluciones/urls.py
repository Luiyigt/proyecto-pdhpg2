from django.urls import path
from . import views

urlpatterns = [
    # Ruta para listar todas las resoluciones
    path('', views.lista_resoluciones, name='lista_resoluciones'),

    # Ruta para ver el detalle de una resolución específica
    path('resolucion/<int:pk>/', views.detalle_resolucion, name='detalle_resolucion'),

    # Ruta para crear una nueva resolución
    path('resolucion/nueva/', views.crear_resolucion, name='crear_resolucion'),

    # Ruta para editar una resolución existente
    path('resolucion/<int:pk>/editar/', views.editar_resolucion, name='editar_resolucion'),

    # Ruta para eliminar una resolución existente
    path('resolucion/<int:pk>/eliminar/', views.eliminar_resolucion, name='eliminar_resolucion'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
]

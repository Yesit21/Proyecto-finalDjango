from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('crear/', views.crear_reserva, name='crear'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('<int:pk>/', views.reserva_detalle, name='detalle'),
    path('<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar'),
    path('lista/', views.reservas_lista, name='lista'),
    path('<int:pk>/actualizar-estado/', views.actualizar_estado_reserva, name='actualizar_estado'),
    path('mesas/', views.mesas_disponibles, name='mesas'),
]

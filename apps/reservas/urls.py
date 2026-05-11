from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('crear/', views.CrearReservaView.as_view(), name='crear'),
    path('lista/', views.ListaReservasView.as_view(), name='lista'),
    path('<int:pk>/', views.DetalleReservaView.as_view(), name='detalle'),
    path('<int:pk>/actualizar/', views.ActualizarReservaView.as_view(), name='actualizar'),
    path('<int:pk>/cancelar/', views.CancelarReservaView.as_view(), name='cancelar'),
]


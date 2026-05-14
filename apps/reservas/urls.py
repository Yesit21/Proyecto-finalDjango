from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('crear/', views.CrearReservaView.as_view(), name='crear'),
    path('lista/', views.ListaReservasView.as_view(), name='lista'),
    path('<int:pk>/', views.DetalleReservaView.as_view(), name='detalle'),
    path('<int:pk>/actualizar/', views.ActualizarReservaView.as_view(), name='actualizar'),
    path('<int:pk>/cancelar/', views.CancelarReservaView.as_view(), name='cancelar'),
    path('mesas/', views.ListaMesasView.as_view(), name='mesas_lista'),
    path('mesas/crear/', views.CrearMesaView.as_view(), name='mesas_crear'),
    path('mesas/<int:pk>/editar/', views.EditarMesaView.as_view(), name='mesas_editar'),
    path('mesas/<int:pk>/eliminar/', views.EliminarMesaView.as_view(), name='mesas_eliminar'),
    path('staff/', views.ListaReservasStaffView.as_view(), name='staff_lista'),
    path('staff/<int:pk>/editar/', views.EditarReservaStaffView.as_view(), name='staff_editar'),
]


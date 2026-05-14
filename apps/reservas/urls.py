from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    # Reservas para clientes
    path('crear/', views.CrearReservaView.as_view(), name='crear'),
    path('lista/', views.ListaReservasView.as_view(), name='lista'),
    path('<int:pk>/', views.DetalleReservaView.as_view(), name='detalle'),
    path('<int:pk>/actualizar/', views.ActualizarReservaView.as_view(), name='actualizar'),
    path('<int:pk>/cancelar/', views.CancelarReservaView.as_view(), name='cancelar'),
    
    # Gestión de Mesas (Staff)
    path('mesas/', views.ListaMesasView.as_view(), name='mesas_lista'),
    path('mesas/disponibles/', views.ListaMesasClienteView.as_view(), name='mesas_disponibles'),
    path('mesas/crear/', views.CrearMesaView.as_view(), name='mesa_crear'),
    path('mesas/<int:pk>/editar/', views.EditarMesaView.as_view(), name='mesa_editar'),
    path('mesas/<int:pk>/eliminar/', views.EliminarMesaView.as_view(), name='mesa_eliminar'),
    
    # Gestión de Reservas (Staff)
    path('staff/', views.ListaReservasStaffView.as_view(), name='staff_lista'),
    path('staff/calendario/', views.CalendarioMesasView.as_view(), name='staff_calendario'),
    path('staff/<int:pk>/asignar-mesa/', views.AsignarMesaView.as_view(), name='staff_asignar_mesa'),
    path('staff/<int:pk>/confirmar/', views.ConfirmarReservaView.as_view(), name='staff_confirmar'),
    path('staff/<int:pk>/completar/', views.CompletarReservaView.as_view(), name='staff_completar'),
]


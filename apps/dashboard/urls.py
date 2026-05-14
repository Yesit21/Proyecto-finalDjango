from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('reportes/', views.reporte_panel, name='reportes'),
    
    # Menú de reportes
    path('reportes/menu/', views.reportes_view, name='reportes_menu'),
    
    # Reportes de Pedidos
    path('reportes/pedidos/pdf/', views.reporte_pedidos_pdf, name='reporte_pedidos_pdf'),
    path('reportes/pedidos/excel/', views.reporte_pedidos_excel, name='reporte_pedidos_excel'),
    
    # Reportes de Ventas
    path('reportes/ventas/pdf/', views.reporte_ventas_pdf, name='reporte_ventas_pdf'),
    path('reportes/ventas/excel/', views.reporte_ventas_excel, name='reporte_ventas_excel'),
    
    # Reportes de Inventario
    path('reportes/inventario/pdf/', views.reporte_inventario_pdf, name='reporte_inventario_pdf'),
    path('reportes/inventario/excel/', views.reporte_inventario_excel, name='reporte_inventario_excel'),
    
    # Reportes de Reservas
    path('reportes/reservas/pdf/', views.reporte_reservas_pdf, name='reporte_reservas_pdf'),
    path('reportes/reservas/excel/', views.reporte_reservas_excel, name='reporte_reservas_excel'),
]

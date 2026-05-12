from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('pdf/', views.export_orders_pdf, name='pdf'),
    path('excel/', views.export_orders_excel, name='excel'),
]

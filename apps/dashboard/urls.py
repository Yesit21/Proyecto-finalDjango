from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('reportes/', views.reporte_panel, name='reportes'),
]

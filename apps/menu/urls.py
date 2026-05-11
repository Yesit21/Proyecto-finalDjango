from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.ListaMenuView.as_view(), name='lista'),
    path('<int:pk>/', views.DetallePlatoView.as_view(), name='detalle'),
]

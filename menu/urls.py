from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='lista'),
    path('plato/<int:pk>/', views.plato_detalle, name='detalle'),
    path('plato/crear/', views.plato_crear, name='crear'),
    path('plato/<int:pk>/editar/', views.plato_editar, name='editar'),
    path('plato/<int:pk>/eliminar/', views.plato_eliminar, name='eliminar'),
    path('ingredientes/', views.ingrediente_lista, name='ingredientes'),
]

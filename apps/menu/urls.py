from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # URLs de Platos (público)
    path('', views.ListaMenuView.as_view(), name='lista'),
    path('<int:pk>/', views.DetallePlatoView.as_view(), name='detalle'),
    
    # URLs de Platos (admin)
    path('platos/admin/', views.ListaPlatosAdminView.as_view(), name='platos_admin'),
    path('platos/crear/', views.CrearPlatoView.as_view(), name='platos_crear'),
    path('platos/<int:pk>/editar/', views.EditarPlatoView.as_view(), name='platos_editar'),
    path('platos/<int:pk>/eliminar/', views.EliminarPlatoView.as_view(), name='platos_eliminar'),
    
    # URLs de Ingredientes
    path('ingredientes/', views.ListaIngredientesView.as_view(), name='ingredientes_lista'),
    path('ingredientes/crear/', views.CrearIngredienteView.as_view(), name='ingredientes_crear'),
    path('ingredientes/<int:pk>/editar/', views.EditarIngredienteView.as_view(), name='ingredientes_editar'),
    path('ingredientes/<int:pk>/eliminar/', views.EliminarIngredienteView.as_view(), name='ingredientes_eliminar'),
    
    # URLs de Ingredientes de Platos
    path('platos/<int:plato_id>/ingredientes/', views.gestionar_ingredientes_plato, name='gestionar_ingredientes_plato'),
    path('platos/ingredientes/<int:plato_ingrediente_id>/eliminar/', views.eliminar_ingrediente_plato, name='eliminar_ingrediente_plato'),
]

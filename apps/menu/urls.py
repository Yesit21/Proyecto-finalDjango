from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.ListaMenuView.as_view(), name='lista'),
    path('<int:pk>/', views.DetallePlatoView.as_view(), name='detalle'),
    path('admin/platos/', views.PlatoAdminListView.as_view(), name='platos_admin'),
    path('admin/platos/crear/', views.PlatoCreateView.as_view(), name='platos_crear'),
    path('admin/platos/<int:pk>/editar/', views.PlatoUpdateView.as_view(), name='platos_editar'),
    path('admin/platos/<int:pk>/eliminar/', views.PlatoDeleteView.as_view(), name='platos_eliminar'),
    path('admin/platos/<int:plato_id>/receta/', views.PlatoIngredienteListView.as_view(), name='receta_lista'),
    path('admin/platos/<int:plato_id>/receta/crear/', views.PlatoIngredienteCreateView.as_view(), name='receta_crear'),
    path('admin/receta/<int:pk>/editar/', views.PlatoIngredienteUpdateView.as_view(), name='receta_editar'),
    path('admin/receta/<int:pk>/eliminar/', views.PlatoIngredienteDeleteView.as_view(), name='receta_eliminar'),
    path('admin/platos/<int:plato_id>/precios/', views.PrecioPlatoListView.as_view(), name='precios_lista'),
    path('admin/platos/<int:plato_id>/precios/crear/', views.PrecioPlatoCreateView.as_view(), name='precios_crear'),
    path('admin/precios/<int:pk>/editar/', views.PrecioPlatoUpdateView.as_view(), name='precios_editar'),
    path('admin/precios/<int:pk>/eliminar/', views.PrecioPlatoDeleteView.as_view(), name='precios_eliminar'),
    path('admin/ingredientes/', views.IngredienteListView.as_view(), name='ingredientes_lista'),
    path('admin/ingredientes/crear/', views.IngredienteCreateView.as_view(), name='ingredientes_crear'),
    path('admin/ingredientes/<int:pk>/editar/', views.IngredienteUpdateView.as_view(), name='ingredientes_editar'),
    path('admin/ingredientes/<int:pk>/eliminar/', views.IngredienteDeleteView.as_view(), name='ingredientes_eliminar'),
]

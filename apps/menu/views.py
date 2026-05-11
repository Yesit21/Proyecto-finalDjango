from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Plato

class ListaMenuView(ListView):
    model = Plato
    template_name = 'menu/lista.html'
    context_object_name = 'platos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Plato.objects.filter(disponible=True)
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Plato.CATEGORIA_CHOICES
        return context

class DetallePlatoView(DetailView):
    model = Plato
    template_name = 'menu/detalle.html'
    context_object_name = 'plato'

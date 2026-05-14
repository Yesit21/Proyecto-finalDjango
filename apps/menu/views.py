from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Plato, Ingrediente, PlatoIngrediente
from .forms import PlatoForm, IngredienteForm, PlatoIngredienteForm


# ==================== MIXINS ====================

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to verify that the user is an administrator"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'administrator'
    
    def handle_no_permission(self):
        return redirect('menu:lista')


# ==================== DISH VIEWS ====================

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get dish ingredients
        context['plato_ingredientes'] = PlatoIngrediente.objects.filter(plato=self.object).select_related('ingrediente')
        return context


class CrearPlatoView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'menu/platos/form.html'
    success_url = reverse_lazy('menu:lista')

    def form_valid(self, form):
        messages.success(self.request, f'Dish "{form.instance.nombre}" created successfully.')
        return super().form_valid(form)


class EditarPlatoView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'menu/platos/form.html'
    success_url = reverse_lazy('menu:lista')

    def form_valid(self, form):
        messages.success(self.request, f'Dish "{form.instance.nombre}" updated successfully.')
        return super().form_valid(form)


class EliminarPlatoView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Plato
    template_name = 'menu/platos/confirmar_eliminar.html'
    success_url = reverse_lazy('menu:lista')

    def delete(self, request, *args, **kwargs):
        plato = self.get_object()
        messages.success(request, f'Dish "{plato.nombre}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ListaPlatosAdminView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Plato
    template_name = 'menu/platos/lista_admin.html'
    context_object_name = 'platos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Plato.objects.all().order_by('categoria', 'nombre')
        buscar = self.request.GET.get('buscar')
        categoria = self.request.GET.get('categoria')
        
        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Plato.CATEGORIA_CHOICES
        return context


# ==================== INGREDIENT VIEWS ====================

class ListaIngredientesView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Ingrediente
    template_name = 'menu/ingredientes/lista.html'
    context_object_name = 'ingredientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Ingrediente.objects.all().order_by('nombre')
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)
        return queryset


class CrearIngredienteView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = 'menu/ingredientes/form.html'
    success_url = reverse_lazy('menu:ingredientes_lista')

    def form_valid(self, form):
        messages.success(self.request, f'Ingredient "{form.instance.nombre}" created successfully.')
        return super().form_valid(form)


class EditarIngredienteView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = 'menu/ingredientes/form.html'
    success_url = reverse_lazy('menu:ingredientes_lista')

    def form_valid(self, form):
        messages.success(self.request, f'Ingredient "{form.instance.nombre}" updated successfully.')
        return super().form_valid(form)


class EliminarIngredienteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Ingrediente
    template_name = 'menu/ingredientes/confirmar_eliminar.html'
    success_url = reverse_lazy('menu:ingredientes_lista')

    def delete(self, request, *args, **kwargs):
        ingrediente = self.get_object()
        messages.success(request, f'Ingredient "{ingrediente.nombre}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


@login_required
def gestionar_ingredientes_plato(request, plato_id):
    """View to manage ingredients for a specific dish"""
    if request.user.rol != 'administrator':
        return redirect('menu:lista')
    
    plato = get_object_or_404(Plato, pk=plato_id)
    plato_ingredientes = PlatoIngrediente.objects.filter(plato=plato).select_related('ingrediente')
    
    if request.method == 'POST':
        form = PlatoIngredienteForm(request.POST)
        if form.is_valid():
            plato_ingrediente = form.save(commit=False)
            plato_ingrediente.plato = plato
            plato_ingrediente.save()
            messages.success(request, f'Ingredient added to dish "{plato.nombre}".')
            return redirect('menu:gestionar_ingredientes_plato', plato_id=plato.id)
    else:
        form = PlatoIngredienteForm()
    
    context = {
        'plato': plato,
        'plato_ingredientes': plato_ingredientes,
        'form': form,
    }
    return render(request, 'menu/ingredientes/gestionar_plato.html', context)


@login_required
def eliminar_ingrediente_plato(request, plato_ingrediente_id):
    """View to remove an ingredient from a dish"""
    if request.user.rol != 'administrator':
        return redirect('menu:lista')
    
    plato_ingrediente = get_object_or_404(PlatoIngrediente, pk=plato_ingrediente_id)
    plato_id = plato_ingrediente.plato.id
    plato_ingrediente.delete()
    messages.success(request, 'Ingredient removed from dish.')
    return redirect('menu:gestionar_ingredientes_plato', plato_id=plato_id)

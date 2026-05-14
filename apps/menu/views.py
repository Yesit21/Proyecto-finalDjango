from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.permissions.base import AdminRequiredMixin
from .forms import IngredienteForm, PlatoForm, PlatoIngredienteForm, PrecioPlatoForm
from .models import Ingrediente, Plato, PlatoIngrediente, PrecioPlato

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


class IngredienteListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Ingrediente
    template_name = "menu/ingredientes/lista.html"
    context_object_name = "ingredientes"
    paginate_by = 20
    raise_exception = True


class IngredienteCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = "menu/ingredientes/form.html"
    success_url = reverse_lazy("menu:ingredientes_lista")
    raise_exception = True


class IngredienteUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = "menu/ingredientes/form.html"
    success_url = reverse_lazy("menu:ingredientes_lista")
    raise_exception = True


class IngredienteDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Ingrediente
    template_name = "menu/ingredientes/confirmar_eliminar.html"
    success_url = reverse_lazy("menu:ingredientes_lista")
    raise_exception = True


class PlatoAdminListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Plato
    template_name = "menu/platos/lista_admin.html"
    context_object_name = "platos"
    paginate_by = 20
    raise_exception = True


class PlatoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = "menu/platos/form.html"
    success_url = reverse_lazy("menu:platos_admin")
    raise_exception = True


class PlatoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = "menu/platos/form.html"
    success_url = reverse_lazy("menu:platos_admin")
    raise_exception = True


class PlatoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Plato
    template_name = "menu/platos/confirmar_eliminar.html"
    success_url = reverse_lazy("menu:platos_admin")
    raise_exception = True


class PlatoIngredienteListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = PlatoIngrediente
    template_name = "menu/recetas/lista.html"
    context_object_name = "items"
    raise_exception = True

    def get_queryset(self):
        return (
            PlatoIngrediente.objects
            .select_related("plato", "ingrediente")
            .filter(plato_id=self.kwargs["plato_id"])
            .order_by("ingrediente__nombre")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plato"] = get_object_or_404(Plato, pk=self.kwargs["plato_id"])
        return context


class PlatoIngredienteCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = PlatoIngrediente
    form_class = PlatoIngredienteForm
    template_name = "menu/recetas/form.html"
    raise_exception = True

    def form_valid(self, form):
        form.instance.plato = get_object_or_404(Plato, pk=self.kwargs["plato_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("menu:receta_lista", kwargs={"plato_id": self.kwargs["plato_id"]})


class PlatoIngredienteUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = PlatoIngrediente
    form_class = PlatoIngredienteForm
    template_name = "menu/recetas/form.html"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("menu:receta_lista", kwargs={"plato_id": self.object.plato_id})


class PlatoIngredienteDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = PlatoIngrediente
    template_name = "menu/recetas/confirmar_eliminar.html"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("menu:receta_lista", kwargs={"plato_id": self.object.plato_id})


class PrecioPlatoListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = PrecioPlato
    template_name = "menu/precios/lista.html"
    context_object_name = "precios"
    raise_exception = True

    def get_queryset(self):
        return PrecioPlato.objects.filter(plato_id=self.kwargs["plato_id"]).order_by("-fecha_inicio")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plato"] = get_object_or_404(Plato, pk=self.kwargs["plato_id"])
        return context


class PrecioPlatoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = PrecioPlato
    form_class = PrecioPlatoForm
    template_name = "menu/precios/form.html"
    raise_exception = True

    def form_valid(self, form):
        plato = get_object_or_404(Plato, pk=self.kwargs["plato_id"])
        form.instance.plato = plato
        PrecioPlato.objects.filter(plato=plato, activo=True).update(activo=False)
        response = super().form_valid(form)
        plato.precio = form.instance.precio
        plato.save(update_fields=["precio"])
        return response

    def get_success_url(self):
        return reverse_lazy("menu:precios_lista", kwargs={"plato_id": self.kwargs["plato_id"]})


class PrecioPlatoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = PrecioPlato
    form_class = PrecioPlatoForm
    template_name = "menu/precios/form.html"
    raise_exception = True

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.activo:
            PrecioPlato.objects.filter(plato=form.instance.plato).exclude(pk=form.instance.pk).update(activo=False)
            form.instance.plato.precio = form.instance.precio
            form.instance.plato.save(update_fields=["precio"])
        return response

    def get_success_url(self):
        return reverse_lazy("menu:precios_lista", kwargs={"plato_id": self.object.plato_id})


class PrecioPlatoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = PrecioPlato
    template_name = "menu/precios/confirmar_eliminar.html"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("menu:precios_lista", kwargs={"plato_id": self.object.plato_id})

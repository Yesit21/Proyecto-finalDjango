from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm

class CrearReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/crear.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Reserva creada exitosamente')
        return super().form_valid(form)

class ListaReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/lista.html'
    context_object_name = 'reservas'
    paginate_by = 10
    login_url = 'usuarios:login'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)

class DetalleReservaView(LoginRequiredMixin, DetailView):
    model = Reserva
    template_name = 'reservas/detalle.html'
    context_object_name = 'reserva'
    login_url = 'usuarios:login'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)

class ActualizarReservaView(LoginRequiredMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/actualizar.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Reserva actualizada exitosamente')
        return super().form_valid(form)

class CancelarReservaView(LoginRequiredMixin, UpdateView):
    model = Reserva
    fields = []
    template_name = 'reservas/confirmar_cancelacion.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user, estado__in=['pendiente', 'confirmada'])

    def form_valid(self, form):
        form.instance.estado = 'cancelada'
        messages.warning(self.request, 'Reserva cancelada')
        return super().form_valid(form)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from core.permissions.base import AdminRequiredMixin, MeseroRequiredMixin
from services.email.email_service import EmailService
from .models import Mesa, Reserva
from .forms import MesaForm, ReservaForm, ReservaStaffForm

class CrearReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/crear.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Reserva creada exitosamente')
        response = super().form_valid(form)
        EmailService.send_reservation_confirmation(self.object)
        return response

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


class ListaReservasStaffView(LoginRequiredMixin, MeseroRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/staff/lista.html'
    context_object_name = 'reservas'
    paginate_by = 20
    raise_exception = True

    def get_queryset(self):
        return Reserva.objects.select_related('usuario', 'mesa').all().order_by('-fecha_reserva')


class EditarReservaStaffView(LoginRequiredMixin, MeseroRequiredMixin, UpdateView):
    model = Reserva
    form_class = ReservaStaffForm
    template_name = 'reservas/staff/editar.html'
    success_url = reverse_lazy('reservas:staff_lista')
    raise_exception = True

    def form_valid(self, form):
        messages.success(self.request, 'Reserva actualizada.')
        return super().form_valid(form)


class ListaMesasView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Mesa
    template_name = "reservas/mesas/lista.html"
    context_object_name = "mesas"
    paginate_by = 20
    raise_exception = True


class CrearMesaView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = "reservas/mesas/form.html"
    success_url = reverse_lazy("reservas:mesas_lista")
    raise_exception = True


class EditarMesaView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = "reservas/mesas/form.html"
    success_url = reverse_lazy("reservas:mesas_lista")
    raise_exception = True


class EliminarMesaView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Mesa
    template_name = "reservas/mesas/confirmar_eliminar.html"
    success_url = reverse_lazy("reservas:mesas_lista")
    raise_exception = True

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from services.email.email_service import EmailService
from .models import Reserva
from .forms import ReservaForm
import logging

logger = logging.getLogger(__name__)

class CrearReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/crear.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        
        # Enviar email de confirmación
        try:
            EmailService.send_reservation_confirmation(self.object)
            logger.info(f"Email de confirmación enviado para reserva #{self.object.id}")
        except Exception as e:
            logger.error(f"Error enviando email de confirmación: {str(e)}")
        
        messages.success(self.request, 'Reserva creada exitosamente')
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
        # Guardar estado anterior
        estado_anterior = self.object.get_estado_display()
        estado_anterior_codigo = self.object.estado
        
        response = super().form_valid(form)
        
        # Enviar email solo si el estado cambió
        if estado_anterior_codigo != self.object.estado:
            try:
                EmailService.send_reservation_status_change(self.object, estado_anterior)
                logger.info(f"Email de cambio de estado enviado para reserva #{self.object.id}")
            except Exception as e:
                logger.error(f"Error enviando email de cambio de estado: {str(e)}")
        
        messages.success(self.request, 'Reserva actualizada exitosamente')
        return response

class CancelarReservaView(LoginRequiredMixin, UpdateView):
    model = Reserva
    fields = []
    template_name = 'reservas/confirmar_cancelacion.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user, estado__in=['pendiente', 'confirmada'])

    def form_valid(self, form):
        # Guardar estado anterior
        estado_anterior = self.object.get_estado_display()
        
        form.instance.estado = 'cancelada'
        response = super().form_valid(form)
        
        # Enviar email de cancelación
        try:
            EmailService.send_reservation_status_change(self.object, estado_anterior)
            logger.info(f"Email de cancelación enviado para reserva #{self.object.id}")
        except Exception as e:
            logger.error(f"Error enviando email de cancelación: {str(e)}")
        
        messages.warning(self.request, 'Reserva cancelada')
        return response

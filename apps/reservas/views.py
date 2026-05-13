from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from services.email.email_service import EmailService
from .models import Reserva, Mesa
from .forms import ReservaForm, MesaForm, AsignarMesaForm
import logging

logger = logging.getLogger(__name__)

class CrearReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/crear.html'
    success_url = reverse_lazy('reservas:lista')
    login_url = 'usuarios:login'

    def get_initial(self):
        initial = super().get_initial()
        mesa_id = self.request.GET.get('mesa')
        if mesa_id:
            initial['mesa'] = mesa_id
        return initial

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
        # Si seleccionó una mesa, marcarla como reservada
        if form.cleaned_data.get('mesa'):
            mesa = form.cleaned_data['mesa']
            mesa.estado = 'reservada'
            mesa.save()
            
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
        # Guardar estado y mesa anterior
        reserva_anterior = self.get_object()
        mesa_anterior = reserva_anterior.mesa
        estado_anterior_codigo = reserva_anterior.estado
        estado_anterior_display = reserva_anterior.get_estado_display()
        
        response = super().form_valid(form)
        nueva_mesa = self.object.mesa
        
        # Si la mesa cambió
        if mesa_anterior != nueva_mesa:
            # Liberar mesa anterior
            if mesa_anterior:
                mesa_anterior.estado = 'disponible'
                mesa_anterior.save()
            
            # Reservar nueva mesa
            if nueva_mesa:
                nueva_mesa.estado = 'reservada'
                nueva_mesa.save()
        
        # Enviar email solo si el estado cambió
        if estado_anterior_codigo != self.object.estado:
            try:
                EmailService.send_reservation_status_change(self.object, estado_anterior_display)
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
        
        # Liberar la mesa si estaba asignada
        if self.object.mesa:
            mesa = self.object.mesa
            mesa.estado = 'disponible'
            mesa.save()
            
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


# ============================================
# VISTAS PARA GESTIÓN DE MESAS (STAFF)
# ============================================

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario sea staff (mesero o administrador)"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol in ['mesero', 'administrador']
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard:home')


class ListaMesasClienteView(LoginRequiredMixin, ListView):
    """Vista para que los clientes vean las mesas disponibles"""
    model = Mesa
    template_name = 'reservas/mesas/lista_cliente.html'
    context_object_name = 'mesas'
    login_url = 'usuarios:login'

    def get_queryset(self):
        return Mesa.objects.filter(activa=True, estado='disponible')


class ListaMesasView(StaffRequiredMixin, ListView):
    model = Mesa
    template_name = 'reservas/mesas/lista.html'
    context_object_name = 'mesas'
    paginate_by = 20
    login_url = 'usuarios:login'

    def get_queryset(self):
        queryset = Mesa.objects.all()
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = Mesa.ESTADO_CHOICES
        
        # Calcular estadísticas para la barra superior
        todas_las_mesas = Mesa.objects.all()
        context['total_mesas'] = todas_las_mesas.count()
        context['disponibles_count'] = todas_las_mesas.filter(estado='disponible').count()
        context['reservadas_count'] = todas_las_mesas.filter(estado='reservada').count()
        context['ocupadas_count'] = todas_las_mesas.filter(estado='ocupada').count()
        
        return context


class CrearMesaView(StaffRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'reservas/mesas/form.html'
    success_url = reverse_lazy('reservas:mesas_lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        messages.success(self.request, 'Mesa creada exitosamente')
        return super().form_valid(form)


class EditarMesaView(StaffRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'reservas/mesas/form.html'
    success_url = reverse_lazy('reservas:mesas_lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        messages.success(self.request, 'Mesa actualizada exitosamente')
        return super().form_valid(form)


class EliminarMesaView(StaffRequiredMixin, DeleteView):
    model = Mesa
    template_name = 'reservas/mesas/confirmar_eliminar.html'
    success_url = reverse_lazy('reservas:mesas_lista')
    login_url = 'usuarios:login'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, 'Mesa eliminada')
        return super().delete(request, *args, **kwargs)

# VISTAS PARA GESTIÓN DE RESERVAS (STAF)

class ListaReservasStaffView(StaffRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/staff/lista_reservas.html'
    context_object_name = 'reservas'
    paginate_by = 20
    login_url = 'usuarios:login'

    def get_queryset(self):
        queryset = Reserva.objects.select_related('usuario', 'mesa').all()
        
        # Filtros
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(usuario__nombre__icontains=buscar) |
                Q(usuario__apellido__icontains=buscar) |
                Q(usuario__email__icontains=buscar)
            )
        
        return queryset.order_by('-fecha_reserva')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = Reserva.ESTADO_CHOICES
        return context


class AsignarMesaView(StaffRequiredMixin, UpdateView):
    model = Reserva
    form_class = AsignarMesaForm
    template_name = 'reservas/staff/asignar_mesa.html'
    success_url = reverse_lazy('reservas:staff_lista')
    login_url = 'usuarios:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mesas_disponibles'] = Mesa.objects.filter(activa=True, estado='disponible')
        return context

    def form_valid(self, form):
        # Guardar estado anterior
        estado_anterior = self.object.get_estado_display()
        estado_anterior_codigo = self.object.estado
        
        # Si se asigna una mesa, actualizar su estado
        if form.cleaned_data.get('mesa'):
            mesa = form.cleaned_data['mesa']
            mesa.estado = 'reservada'
            mesa.save()
            
            # Si había una mesa anterior asignada, liberarla
            if self.object.mesa and self.object.mesa != mesa:
                mesa_anterior = self.object.mesa
                mesa_anterior.estado = 'disponible'
                mesa_anterior.save()
        
        response = super().form_valid(form)
        
        # Enviar email si el estado cambió
        if estado_anterior_codigo != self.object.estado:
            try:
                EmailService.send_reservation_status_change(self.object, estado_anterior)
                logger.info(f"Email de cambio de estado enviado para reserva #{self.object.id}")
            except Exception as e:
                logger.error(f"Error enviando email de cambio de estado: {str(e)}")
        
        messages.success(self.request, 'Reserva actualizada y mesa asignada exitosamente')
        return response


class ConfirmarReservaView(StaffRequiredMixin, UpdateView):
    model = Reserva
    fields = []
    template_name = 'reservas/staff/confirmar_reserva.html'
    success_url = reverse_lazy('reservas:staff_lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        # Guardar estado anterior
        estado_anterior = self.object.get_estado_display()
        
        form.instance.estado = 'confirmada'
        response = super().form_valid(form)
        
        # Enviar email de confirmación
        try:
            EmailService.send_reservation_status_change(self.object, estado_anterior)
            logger.info(f"Email de confirmación enviado para reserva #{self.object.id}")
        except Exception as e:
            logger.error(f"Error enviando email de confirmación: {str(e)}")
        
        messages.success(self.request, 'Reserva confirmada exitosamente')
        return response


class CompletarReservaView(StaffRequiredMixin, UpdateView):
    model = Reserva
    fields = []
    template_name = 'reservas/staff/completar_reserva.html'
    success_url = reverse_lazy('reservas:staff_lista')
    login_url = 'usuarios:login'

    def form_valid(self, form):
        form.instance.estado = 'completada'
        
        # Liberar la mesa si estaba asignada
        if self.object.mesa:
            mesa = self.object.mesa
            mesa.estado = 'disponible'
            mesa.save()
        
        response = super().form_valid(form)
        messages.success(self.request, 'Reserva completada y mesa liberada')
        return response


class CalendarioMesasView(StaffRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/staff/calendario.html'
    context_object_name = 'reservas'
    login_url = 'usuarios:login'

    def get_queryset(self):
        # Obtener reservas confirmadas y pendientes
        return Reserva.objects.filter(
            estado__in=['pendiente', 'confirmada']
        ).select_related('usuario', 'mesa').order_by('fecha_reserva')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mesas'] = Mesa.objects.filter(activa=True)
        return context

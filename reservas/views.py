from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Reserva, Mesa
from .forms import ReservaForm

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.save()
            
            send_mail(
                'Confirmación de Reserva',
                f'Tu reserva para {reserva.numero_personas} personas el {reserva.fecha_reserva} a las {reserva.hora_reserva} ha sido registrada.',
                'noreply@restaurante.com',
                [request.user.email],
            )
            
            messages.success(request, 'Reserva creada exitosamente')
            return redirect('reservas:mis_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/crear.html', {'form': form})

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user).order_by('-fecha_reserva')
    return render(request, 'reservas/mis_reservas.html', {'reservas': reservas})

@login_required
def reserva_detalle(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.cliente != request.user and request.user.rol not in ['mesero', 'administrador']:
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    return render(request, 'reservas/detalle.html', {'reserva': reserva})

@login_required
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, cliente=request.user)
    if request.method == 'POST':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.success(request, 'Reserva cancelada')
        return redirect('reservas:mis_reservas')
    return render(request, 'reservas/cancelar.html', {'reserva': reserva})

@login_required
def reservas_lista(request):
    if request.user.rol not in ['mesero', 'administrador']:
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    return render(request, 'reservas/lista.html', {'reservas': reservas})

@login_required
def actualizar_estado_reserva(request, pk):
    if request.user.rol not in ['mesero', 'administrador']:
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        reserva.estado = nuevo_estado
        reserva.save()
        messages.success(request, 'Estado actualizado')
    return redirect('reservas:detalle', pk=pk)

def mesas_disponibles(request):
    mesas = Mesa.objects.filter(activa=True)
    return render(request, 'reservas/mesas.html', {'mesas': mesas})

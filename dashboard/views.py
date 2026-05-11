from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from pedidos.models import Pedido, DetallePedido
from reservas.models import Reserva
from menu.models import Plato, Ingrediente
from usuarios.models import Usuario
import json

@login_required
def home(request):
    context = {}
    
    if request.user.rol == 'cliente':
        context['pedidos_recientes'] = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')[:5]
        context['reservas_proximas'] = Reserva.objects.filter(
            cliente=request.user,
            fecha_reserva__gte=timezone.now().date()
        ).order_by('fecha_reserva')[:5]
    
    elif request.user.rol in ['mesero', 'administrador']:
        hoy = timezone.now().date()
        context['pedidos_hoy'] = Pedido.objects.filter(fecha_pedido__date=hoy).count()
        context['ventas_hoy'] = Pedido.objects.filter(
            fecha_pedido__date=hoy,
            pagado=True
        ).aggregate(total=Sum('total'))['total'] or 0
        context['reservas_hoy'] = Reserva.objects.filter(fecha_reserva=hoy).count()
        context['pedidos_pendientes'] = Pedido.objects.filter(
            estado__in=['pendiente', 'en_preparacion']
        ).count()
    
    return render(request, 'dashboard/home.html', context)

@login_required
def reportes(request):
    if request.user.rol != 'administrador':
        return redirect('dashboard:home')
    
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)
    
    ventas_diarias = Pedido.objects.filter(
        fecha_pedido__date=hoy,
        pagado=True
    ).aggregate(total=Sum('total'))['total'] or 0
    
    platos_vendidos = DetallePedido.objects.filter(
        pedido__fecha_pedido__date__gte=hace_30_dias
    ).values('plato__nombre').annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:10]
    
    ingresos_mensuales = []
    for i in range(30):
        fecha = hoy - timedelta(days=i)
        ingreso = Pedido.objects.filter(
            fecha_pedido__date=fecha,
            pagado=True
        ).aggregate(total=Sum('total'))['total'] or 0
        ingresos_mensuales.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'ingreso': float(ingreso)
        })
    ingresos_mensuales.reverse()
    
    ingredientes_bajo_stock = Ingrediente.objects.filter(
        stock_actual__lte=F('stock_minimo')
    )
    
    context = {
        'ventas_diarias': ventas_diarias,
        'platos_vendidos': platos_vendidos,
        'platos_vendidos_json': json.dumps(list(platos_vendidos)),
        'ingresos_mensuales_json': json.dumps(ingresos_mensuales),
        'ingredientes_bajo_stock': ingredientes_bajo_stock,
    }
    
    return render(request, 'dashboard/reportes.html', context)

@login_required
def estadisticas(request):
    if request.user.rol != 'administrador':
        return redirect('dashboard:home')
    
    total_pedidos = Pedido.objects.count()
    total_clientes = Usuario.objects.filter(rol='cliente').count()
    total_platos = Plato.objects.count()
    total_reservas = Reserva.objects.count()
    
    context = {
        'total_pedidos': total_pedidos,
        'total_clientes': total_clientes,
        'total_platos': total_platos,
        'total_reservas': total_reservas,
    }
    
    return render(request, 'dashboard/estadisticas.html', context)

import json
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import Coalesce, TruncDate
from django.shortcuts import render
from django.utils import timezone
from apps.inventario.models import Producto
from apps.pedidos.models import Pedido, PedidoItem


@login_required
def home(request):
    if getattr(request.user, "rol", None) not in {"mesero", "administrador"}:
        raise PermissionDenied
    now = timezone.now()
    fecha_inicio = now - timedelta(days=30)

    pedidos_ultimos = Pedido.objects.filter(fecha_pedido__gte=fecha_inicio)
    total_pedidos = pedidos_ultimos.count()
    ingresos = pedidos_ultimos.aggregate(total=Sum('total'))['total'] or 0
    promedio_por_pedido = pedidos_ultimos.aggregate(promedio=Avg('total'))['promedio'] or 0
    pedidos_por_estado = Pedido.objects.values('estado').annotate(count=Count('id'))
    productos_bajos = Producto.objects.filter(stock_actual__lte=F('alerta_stock')).count()
    platos_vendidos = (
        PedidoItem.objects
        .annotate(nombre_plato=Coalesce('producto__plato__nombre', 'nombre'))
        .values('nombre_plato')
        .annotate(cantidad=Sum('cantidad'))
        .order_by('-cantidad')[:5]
    )

    ventas_por_dia = (
        pedidos_ultimos
        .annotate(dia=TruncDate('fecha_pedido'))
        .values('dia')
        .annotate(total=Sum('total'))
        .order_by('dia')
    )

    datos_ventas = json.dumps([item['total'] or 0 for item in ventas_por_dia])
    etiquetas_ventas = json.dumps([item['dia'].strftime('%Y-%m-%d') for item in ventas_por_dia])
    datos_pedidos = json.dumps([item['count'] for item in pedidos_por_estado])
    etiquetas_pedidos = json.dumps([item['estado'] for item in pedidos_por_estado])
    datos_platos = json.dumps([item['cantidad'] for item in platos_vendidos])
    etiquetas_platos = json.dumps([item['nombre_plato'] for item in platos_vendidos])

    context = {
        'total_pedidos': total_pedidos,
        'ingresos': ingresos,
        'promedio_por_pedido': promedio_por_pedido,
        'productos_bajos': productos_bajos,
        'ventas_por_dia': ventas_por_dia,
        'etiquetas_ventas': etiquetas_ventas,
        'datos_ventas': datos_ventas,
        'etiquetas_pedidos': etiquetas_pedidos,
        'datos_pedidos': datos_pedidos,
        'etiquetas_platos': etiquetas_platos,
        'datos_platos': datos_platos,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def reporte_panel(request):
    if getattr(request.user, "rol", None) not in {"mesero", "administrador"}:
        raise PermissionDenied
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    if fecha_desde:
        pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
    if fecha_hasta:
        pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)

    datos = {
        'pedidos': pedidos,
        'desde': fecha_desde,
        'hasta': fecha_hasta,
    }
    return render(request, 'dashboard/reportes.html', datos)

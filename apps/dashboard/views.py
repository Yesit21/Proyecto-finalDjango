import json
import logging
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from apps.inventario.models import Producto
from apps.pedidos.models import Pedido, PedidoItem
from apps.reservas.models import Reserva
from services.reports.pdf_service import PDFService
from services.reports.excel_service import ExcelService

logger = logging.getLogger(__name__)


@login_required
def home(request):
    # Solo meseros y administradores pueden ver el dashboard
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para acceder al dashboard.')
        return redirect(reverse('menu:lista'))
    
    now = timezone.now()
    fecha_inicio = now - timedelta(days=30)

    pedidos_ultimos = Pedido.objects.filter(fecha_pedido__gte=fecha_inicio)
    total_pedidos = pedidos_ultimos.count()
    ingresos = pedidos_ultimos.aggregate(total=Sum('total'))['total'] or 0
    promedio_por_pedido = pedidos_ultimos.aggregate(promedio=Avg('total'))['promedio'] or 0
    pedidos_por_estado = Pedido.objects.values('estado').annotate(count=Count('id'))
    productos_bajos = Producto.objects.filter(stock_actual__lte=F('alerta_stock')).count()
    platos_vendidos = PedidoItem.objects.values('nombre').annotate(cantidad=Sum('cantidad')).order_by('-cantidad')[:5]

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
    etiquetas_platos = json.dumps([item['nombre'] for item in platos_vendidos])

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
    # Solo administradores pueden ver reportes
    if request.user.rol != 'administrador':
        messages.warning(request, 'No tienes permiso para acceder a los reportes.')
        return redirect(reverse('dashboard:home'))
    
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



# ==================== VISTAS DE REPORTES ====================

@login_required
def reportes_view(request):
    """Vista principal de reportes"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para acceder a los reportes.')
        return redirect(reverse('menu:lista'))
    
    context = {
        'page_title': 'Reportes',
    }
    return render(request, 'dashboard/reportes_menu.html', context)


@login_required
def reporte_pedidos_pdf(request):
    """Genera reporte de pedidos en PDF"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para generar reportes.')
        return redirect(reverse('menu:lista'))
    
    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        estado = request.GET.get('estado')
        
        # Construir queryset
        pedidos = Pedido.objects.all().order_by('-fecha_pedido')
        
        filtros = {}
        if fecha_desde:
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        if estado:
            pedidos = pedidos.filter(estado=estado)
            filtros['estado'] = estado
        
        # Generar PDF
        pdf_buffer = PDFService.generate_orders_report_pdf(pedidos, filtros, request.user)
        
        # Registrar en log
        logger.info(f"Reporte de pedidos generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        filename = f"reporte_pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de pedidos PDF: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_pedidos_excel(request):
    """Genera reporte de pedidos en Excel"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para generar reportes.')
        return redirect(reverse('menu:lista'))
    
    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        estado = request.GET.get('estado')
        
        # Construir queryset
        pedidos = Pedido.objects.all().order_by('-fecha_pedido')
        
        filtros = {}
        if fecha_desde:
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        if estado:
            pedidos = pedidos.filter(estado=estado)
            filtros['estado'] = estado
        
        # Generar Excel
        excel_buffer = ExcelService.generate_orders_report_excel(pedidos, filtros)
        
        # Registrar en log
        logger.info(f"Reporte de pedidos Excel generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"reporte_pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de pedidos Excel: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_ventas_pdf(request):
    """Genera reporte de ventas en PDF"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para generar reportes.')
        return redirect(reverse('menu:lista'))
    
    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        categoria = request.GET.get('categoria')
        
        # Construir queryset
        pedidos = Pedido.objects.filter(estado='completado')
        
        filtros = {}
        if fecha_desde:
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        else:
            # Por defecto, últimos 30 días
            fecha_desde = (timezone.now() - timedelta(days=30)).date()
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde.strftime('%Y-%m-%d')
        
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        else:
            filtros['fecha_hasta'] = timezone.now().date().strftime('%Y-%m-%d')
        
        # Calcular métricas
        total_ingresos = pedidos.aggregate(total=Sum('total'))['total'] or 0
        cantidad_pedidos = pedidos.count()
        ticket_promedio = total_ingresos / cantidad_pedidos if cantidad_pedidos > 0 else 0
        
        # Top platos
        platos_query = PedidoItem.objects.filter(pedido__in=pedidos)
        
        if categoria:
            platos_query = platos_query.filter(plato__categoria=categoria)
            filtros['categoria'] = categoria
        
        platos_mas_vendidos = (
            platos_query
            .values('nombre')
            .annotate(
                cantidad=Sum('cantidad'),
                ingresos=Sum(F('cantidad') * F('precio_unitario'))
            )
            .order_by('-cantidad')
        )
        
        datos_ventas = {
            'total_ingresos': total_ingresos,
            'cantidad_pedidos': cantidad_pedidos,
            'ticket_promedio': ticket_promedio,
            'platos_mas_vendidos': list(platos_mas_vendidos)
        }
        
        # Generar PDF
        pdf_buffer = PDFService.generate_sales_report_pdf(datos_ventas, filtros, request.user)
        
        # Registrar en log
        logger.info(f"Reporte de ventas generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        filename = f"reporte_ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de ventas PDF: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_ventas_excel(request):
    """Genera reporte de ventas en Excel"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para generar reportes.')
        return redirect(reverse('menu:lista'))
    
    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        categoria = request.GET.get('categoria')
        
        # Construir queryset
        pedidos = Pedido.objects.filter(estado='completado')
        
        filtros = {}
        if fecha_desde:
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        else:
            fecha_desde = (timezone.now() - timedelta(days=30)).date()
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde.strftime('%Y-%m-%d')
        
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        else:
            filtros['fecha_hasta'] = timezone.now().date().strftime('%Y-%m-%d')
        
        # Calcular métricas
        total_ingresos = pedidos.aggregate(total=Sum('total'))['total'] or 0
        cantidad_pedidos = pedidos.count()
        ticket_promedio = total_ingresos / cantidad_pedidos if cantidad_pedidos > 0 else 0
        
        # Top platos
        platos_query = PedidoItem.objects.filter(pedido__in=pedidos)
        
        if categoria:
            platos_query = platos_query.filter(plato__categoria=categoria)
            filtros['categoria'] = categoria
        
        platos_mas_vendidos = (
            platos_query
            .values('nombre')
            .annotate(
                cantidad=Sum('cantidad'),
                ingresos=Sum(F('cantidad') * F('precio_unitario'))
            )
            .order_by('-cantidad')
        )
        
        datos_ventas = {
            'total_ingresos': total_ingresos,
            'cantidad_pedidos': cantidad_pedidos,
            'ticket_promedio': ticket_promedio,
            'platos_mas_vendidos': list(platos_mas_vendidos)
        }
        
        # Generar Excel
        excel_buffer = ExcelService.generate_sales_report_excel(datos_ventas, filtros)
        
        # Registrar en log
        logger.info(f"Reporte de ventas Excel generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"reporte_ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de ventas Excel: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_inventario_pdf(request):
    """Genera reporte de inventario en PDF"""
    if request.user.rol != 'administrador':
        messages.warning(request, 'No tienes permiso para generar reportes de inventario.')
        return redirect(reverse('dashboard:home'))
    
    try:
        # Obtener filtros
        stock_bajo = request.GET.get('stock_bajo')
        
        # Construir queryset
        productos = Producto.objects.all().order_by('nombre')
        
        filtros = {}
        if stock_bajo == 'true':
            productos = productos.filter(stock_actual__lte=F('alerta_stock'))
            filtros['stock_bajo'] = True
        
        # Generar PDF
        pdf_buffer = PDFService.generate_inventory_report_pdf(productos, filtros, request.user)
        
        # Registrar en log
        logger.info(f"Reporte de inventario generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        filename = f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de inventario PDF: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_inventario_excel(request):
    """Genera reporte de inventario en Excel"""
    if request.user.rol != 'administrador':
        messages.warning(request, 'No tienes permiso para generar reportes de inventario.')
        return redirect(reverse('dashboard:home'))
    
    try:
        # Obtener filtros
        stock_bajo = request.GET.get('stock_bajo')
        
        # Construir queryset
        productos = Producto.objects.all().order_by('nombre')
        
        filtros = {}
        if stock_bajo == 'true':
            productos = productos.filter(stock_actual__lte=F('alerta_stock'))
            filtros['stock_bajo'] = True
        
        # Generar Excel
        excel_buffer = ExcelService.generate_inventory_report_excel(productos, filtros)
        
        # Registrar en log
        logger.info(f"Reporte de inventario Excel generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de inventario Excel: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_reservas_pdf(request):
    """Genera reporte de reservas en PDF"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para generar reportes.')
        return redirect(reverse('menu:lista'))
    
    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        estado = request.GET.get('estado')
        
        # Construir queryset
        reservas = Reserva.objects.all().order_by('-fecha_reserva')
        
        filtros = {}
        if fecha_desde:
            reservas = reservas.filter(fecha_reserva__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        if fecha_hasta:
            reservas = reservas.filter(fecha_reserva__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        if estado:
            reservas = reservas.filter(estado=estado)
            filtros['estado'] = estado
        
        # Generar PDF
        pdf_buffer = PDFService.generate_reservations_report_pdf(reservas, filtros, request.user)
        
        # Registrar en log
        logger.info(f"Reporte de reservas generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        filename = f"reporte_reservas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de reservas PDF: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))


@login_required
def reporte_reservas_excel(request):
    """Genera reporte de reservas en Excel"""
    if request.user.rol not in ['mesero', 'administrador']:
        messages.warning(request, 'No tienes permiso para generar reportes.')
        return redirect(reverse('menu:lista'))
    
    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        estado = request.GET.get('estado')
        
        # Construir queryset
        reservas = Reserva.objects.all().order_by('-fecha_reserva')
        
        filtros = {}
        if fecha_desde:
            reservas = reservas.filter(fecha_reserva__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        if fecha_hasta:
            reservas = reservas.filter(fecha_reserva__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        if estado:
            reservas = reservas.filter(estado=estado)
            filtros['estado'] = estado
        
        # Generar Excel
        excel_buffer = ExcelService.generate_reservations_report_excel(reservas, filtros)
        
        # Registrar en log
        logger.info(f"Reporte de reservas Excel generado por {request.user.username}")
        
        # Preparar respuesta
        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"reporte_reservas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error generando reporte de reservas Excel: {str(e)}")
        messages.error(request, 'Error al generar el reporte. Por favor, intenta nuevamente.')
        return redirect(reverse('dashboard:reportes'))

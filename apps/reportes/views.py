from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from apps.pedidos.models import Pedido
from .services import PDFReportService
from services.exports.excel_service import ExcelService


def _get_filtered_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').all().order_by('-fecha_pedido')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if desde:
        fecha_desde = parse_date(desde)
        if fecha_desde:
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
    if hasta:
        fecha_hasta = parse_date(hasta)
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)

    return pedidos


@require_http_methods(['GET'])
@login_required
def export_orders_pdf(request):
    if getattr(request.user, "rol", None) not in {"mesero", "administrador"}:
        raise PermissionDenied
    pedidos = _get_filtered_pedidos(request)
    buffer = PDFReportService.generate_orders_report_pdf(pedidos)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reportes_pedidos.pdf'
    return response


@require_http_methods(['GET'])
@login_required
def export_orders_excel(request):
    if getattr(request.user, "rol", None) not in {"mesero", "administrador"}:
        raise PermissionDenied
    pedidos = _get_filtered_pedidos(request)
    buffer = ExcelService.export_orders(pedidos)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reportes_pedidos.xlsx'
    return response

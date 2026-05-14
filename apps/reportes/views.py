from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from apps.pedidos.models import Pedido
from .services import PDFReportService
from services.exports.excel_service import ExcelService


def _get_filtered_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').all().order_by('-fecha_pedido')
    date_from = request.GET.get('desde')
    date_to = request.GET.get('hasta')

    if date_from:
        fecha_desde = parse_date(date_from)
        if fecha_desde:
            pedidos = pedidos.filter(fecha_pedido__date__gte=fecha_desde)
    if date_to:
        fecha_hasta = parse_date(date_to)
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_pedido__date__lte=fecha_hasta)

    return pedidos


@require_http_methods(['GET'])
def export_orders_pdf(request):
    pedidos = _get_filtered_pedidos(request)
    buffer = PDFReportService.generate_orders_report_pdf(pedidos)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=orders_reports.pdf'
    return response


@require_http_methods(['GET'])
def export_orders_excel(request):
    pedidos = _get_filtered_pedidos(request)
    buffer = ExcelService.export_orders(pedidos)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=orders_reports.xlsx'
    return response

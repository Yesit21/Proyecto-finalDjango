from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from django.conf import settings
import os


class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado para agregar números de página"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.drawRightString(
            letter[0] - 0.75 * inch,
            0.5 * inch,
            f"Página {self._pageNumber} de {page_count}"
        )


class PDFService:
    """Servicio para generación de reportes en PDF"""
    
    @staticmethod
    def _get_logo_path():
        """Obtiene la ruta del logo del restaurante"""
        logo_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            return logo_path
        return None

    @staticmethod
    def _add_header(elements, title, user, styles):
        """Agrega encabezado al reporte"""
        # Logo (si existe)
        logo_path = PDFService._get_logo_path()
        if logo_path:
            try:
                logo = Image(logo_path, width=1*inch, height=1*inch)
                elements.append(logo)
                elements.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#d97706'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(title, title_style))
        
        # Información de generación
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M')
        info_text = f"Generado por: {user.get_full_name() or user.username} | Fecha: {fecha_generacion}"
        elements.append(Paragraph(info_text, info_style))
        elements.append(Spacer(1, 0.3*inch))

    @staticmethod
    def _format_currency(value):
        """Formatea valores monetarios"""
        try:
            return f"${float(value):,.2f}"
        except:
            return "$0.00"

    @staticmethod
    def _format_date(date):
        """Formatea fechas"""
        if date:
            return date.strftime('%d/%m/%Y %H:%M')
        return "N/A"

    @staticmethod
    def generate_order_pdf(pedido):
        """Genera PDF de un pedido individual"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph(f'Pedido #{pedido.id}', styles['Title']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Información del cliente
        elements.append(Paragraph(f'Cliente: {pedido.usuario.get_full_name() or pedido.usuario.username}', styles['Normal']))
        elements.append(Paragraph(f'Fecha: {PDFService._format_date(pedido.fecha_pedido)}', styles['Normal']))
        elements.append(Paragraph(f'Estado: {pedido.get_estado_display()}', styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabla de items
        data = [['Plato', 'Cantidad', 'Precio Unit.', 'Subtotal']]
        for item in pedido.items.all():
            data.append([
                item.nombre,
                str(item.cantidad),
                PDFService._format_currency(item.precio_unitario),
                PDFService._format_currency(item.subtotal)
            ])
        
        table = Table(data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Total
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#d97706'),
            alignment=TA_RIGHT
        )
        elements.append(Paragraph(f'<b>Total: {PDFService._format_currency(pedido.total)}</b>', total_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_orders_report_pdf(pedidos, filtros, user):
        """Genera reporte de pedidos en PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Encabezado
        PDFService._add_header(elements, "Reporte de Pedidos", user, styles)
        
        # Filtros aplicados
        if filtros:
            filtros_text = "Filtros aplicados: "
            if filtros.get('fecha_desde'):
                filtros_text += f"Desde {filtros['fecha_desde']} "
            if filtros.get('fecha_hasta'):
                filtros_text += f"Hasta {filtros['fecha_hasta']} "
            if filtros.get('estado'):
                filtros_text += f"Estado: {filtros['estado']} "
            
            elements.append(Paragraph(filtros_text, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Resumen
        total_pedidos = len(pedidos)
        total_ingresos = sum(p.total for p in pedidos)
        
        summary_data = [
            ['Total de Pedidos', str(total_pedidos)],
            ['Total de Ingresos', PDFService._format_currency(total_ingresos)]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d97706'))
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabla de pedidos
        data = [['#', 'Cliente', 'Fecha', 'Estado', 'Total']]
        for pedido in pedidos:
            data.append([
                str(pedido.id),
                pedido.usuario.get_full_name() or pedido.usuario.username,
                PDFService._format_date(pedido.fecha_pedido),
                pedido.get_estado_display(),
                PDFService._format_currency(pedido.total)
            ])
        
        table = Table(data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1.2*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(table)
        
        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_sales_report_pdf(datos_ventas, filtros, user):
        """Genera reporte de ventas en PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Encabezado
        PDFService._add_header(elements, "Reporte de Ventas", user, styles)
        
        # Período
        periodo_text = f"Período: {filtros.get('fecha_desde', 'Inicio')} - {filtros.get('fecha_hasta', 'Hoy')}"
        elements.append(Paragraph(periodo_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Métricas principales
        metrics_data = [
            ['Métrica', 'Valor'],
            ['Total de Ingresos', PDFService._format_currency(datos_ventas['total_ingresos'])],
            ['Cantidad de Pedidos', str(datos_ventas['cantidad_pedidos'])],
            ['Ticket Promedio', PDFService._format_currency(datos_ventas['ticket_promedio'])],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef3c7')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d97706')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Top 10 platos más vendidos
        elements.append(Paragraph('<b>Top 10 Platos Más Vendidos</b>', styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        platos_data = [['#', 'Plato', 'Cantidad', 'Ingresos']]
        for idx, plato in enumerate(datos_ventas['platos_mas_vendidos'][:10], 1):
            platos_data.append([
                str(idx),
                plato['nombre'],
                str(plato['cantidad']),
                PDFService._format_currency(plato['ingresos'])
            ])
        
        platos_table = Table(platos_data, colWidths=[0.5*inch, 3*inch, 1*inch, 1.5*inch])
        platos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (2, 1), (3, -1), 'RIGHT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(platos_table)
        
        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_inventory_report_pdf(productos, filtros, user):
        """Genera reporte de inventario en PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Encabezado
        PDFService._add_header(elements, "Reporte de Inventario", user, styles)
        
        # Resumen
        total_productos = len(productos)
        productos_bajo_stock = sum(1 for p in productos if p.stock_actual <= p.alerta_stock)
        valor_total = sum(p.stock_actual * p.precio for p in productos)
        
        summary_data = [
            ['Total de Productos', str(total_productos)],
            ['Productos con Stock Bajo', str(productos_bajo_stock)],
            ['Valor Total del Inventario', PDFService._format_currency(valor_total)]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d97706'))
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabla de productos
        data = [['Producto', 'Stock Actual', 'Alerta', 'Precio', 'Valor']]
        for producto in productos:
            bajo_stock = producto.stock_actual <= producto.alerta_stock
            data.append([
                producto.nombre,
                str(producto.stock_actual),
                str(producto.alerta_stock),
                PDFService._format_currency(producto.precio),
                PDFService._format_currency(producto.stock_actual * producto.precio)
            ])
        
        table = Table(data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        
        # Estilo base
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]
        
        # Resaltar productos con stock bajo
        for idx, producto in enumerate(productos, 1):
            if producto.stock_actual <= producto.alerta_stock:
                table_style.append(('TEXTCOLOR', (0, idx), (-1, idx), colors.red))
                table_style.append(('FONTNAME', (0, idx), (-1, idx), 'Helvetica-Bold'))
        
        table.setStyle(TableStyle(table_style))
        elements.append(table)
        
        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_reservations_report_pdf(reservas, filtros, user):
        """Genera reporte de reservas en PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Encabezado
        PDFService._add_header(elements, "Reporte de Reservas", user, styles)
        
        # Filtros aplicados
        if filtros:
            filtros_text = "Filtros aplicados: "
            if filtros.get('fecha_desde'):
                filtros_text += f"Desde {filtros['fecha_desde']} "
            if filtros.get('fecha_hasta'):
                filtros_text += f"Hasta {filtros['fecha_hasta']} "
            if filtros.get('estado'):
                filtros_text += f"Estado: {filtros['estado']} "
            
            elements.append(Paragraph(filtros_text, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Resumen
        total_reservas = len(reservas)
        total_personas = sum(r.cantidad_personas for r in reservas)
        
        summary_data = [
            ['Total de Reservas', str(total_reservas)],
            ['Total de Personas', str(total_personas)]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d97706'))
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabla de reservas
        data = [['#', 'Cliente', 'Fecha', 'Personas', 'Estado']]
        for reserva in reservas:
            data.append([
                str(reserva.id),
                reserva.usuario.get_full_name() or reserva.usuario.username,
                PDFService._format_date(reserva.fecha_reserva),
                str(reserva.cantidad_personas),
                reserva.get_estado_display()
            ])
        
        table = Table(data, colWidths=[0.5*inch, 2*inch, 1.8*inch, 1*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(table)
        
        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer

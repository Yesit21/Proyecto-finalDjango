from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

class PDFService:
    @staticmethod
    def generate_order_pdf(pedido):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph(f'Pedido #{pedido.id}', styles['Title']))
        elements.append(Spacer(1, 0.2*inch))
        
        data = [['Plato', 'Cantidad', 'Precio', 'Subtotal']]
        for item in pedido.items.all():
            data.append([
                item.nombre,  # Corregido: usar item.nombre en lugar de item.plato.nombre
                str(item.cantidad),
                f'${item.precio_unitario}',
                f'${item.subtotal}'
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(f'Total: ${pedido.total}', styles['Heading2']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer

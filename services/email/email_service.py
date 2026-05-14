from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_order_confirmation(pedido):
        destinatario = getattr(pedido.cliente, 'email', '') if pedido and getattr(pedido, 'cliente', None) else ''
        if not destinatario:
            return
        try:
            subject = f'Confirmación de Pedido #{pedido.id}'
            message = render_to_string('emails/order_confirmation.html', {'pedido': pedido})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [destinatario], fail_silently=False)
        except Exception as e:
            logger.error(f'Error enviando confirmación de pedido #{pedido.id}: {str(e)}')
    
    @staticmethod
    def send_reservation_confirmation(reserva):
        destinatario = getattr(reserva.usuario, 'email', '') if reserva and getattr(reserva, 'usuario', None) else ''
        if not destinatario:
            return
        try:
            subject = f'Confirmación de Reserva #{reserva.id}'
            message = render_to_string('emails/reservation_confirmation.html', {'reserva': reserva})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [destinatario], fail_silently=False)
        except Exception as e:
            logger.error(f'Error enviando confirmación de reserva #{reserva.id}: {str(e)}')

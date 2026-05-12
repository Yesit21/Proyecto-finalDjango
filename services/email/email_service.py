from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class EmailService:
    @staticmethod
    def send_order_confirmation(pedido):
        subject = f'Confirmación de Pedido #{pedido.id}'
        message = render_to_string('emails/order_confirmation.html', {'pedido': pedido})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [pedido.cliente.email])
    
    @staticmethod
    def send_reservation_confirmation(reserva):
        subject = f'Confirmación de Reserva #{reserva.id}'
        message = render_to_string('emails/reservation_confirmation.html', {'reserva': reserva})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [reserva.usuario.email])  # Corregido: usuario en lugar de cliente

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Servicio para envío de emails automáticos del sistema.
    Soporta emails en HTML con fallback a texto plano.
    """
    
    @staticmethod
    def _send_html_email(subject, html_content, recipient_list):
        """
        Método interno para enviar emails HTML con fallback a texto plano.
        """
        try:
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_list
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            logger.info(f"Email enviado: {subject} a {recipient_list}")
            return True
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False
    
    @staticmethod
    def send_order_confirmation(pedido):
        """
        Envía email de confirmación cuando se crea un pedido.
        """
        try:
            subject = f'✅ Confirmación de Pedido #{pedido.id} - Restaurante'
            html_content = render_to_string('emails/order_confirmation.html', {
                'pedido': pedido,
                'cliente': pedido.cliente,
                'items': pedido.items.all()
            })
            return EmailService._send_html_email(
                subject, 
                html_content, 
                [pedido.cliente.email]
            )
        except Exception as e:
            logger.error(f"Error en send_order_confirmation: {str(e)}")
            return False
    
    @staticmethod
    def send_order_status_change(pedido, estado_anterior):
        """
        Envía email cuando cambia el estado de un pedido.
        """
        try:
            # Mapeo de estados a emojis y mensajes
            estado_info = {
                'pendiente': {'emoji': '⏳', 'mensaje': 'Tu pedido está pendiente de confirmación'},
                'en_preparacion': {'emoji': '👨‍🍳', 'mensaje': 'Tu pedido está siendo preparado'},
                'listo': {'emoji': '✅', 'mensaje': 'Tu pedido está listo para recoger'},
                'entregado': {'emoji': '🎉', 'mensaje': 'Tu pedido ha sido entregado'},
                'cancelado': {'emoji': '❌', 'mensaje': 'Tu pedido ha sido cancelado'},
            }
            
            info = estado_info.get(pedido.estado, {'emoji': '📦', 'mensaje': 'Estado actualizado'})
            
            subject = f"{info['emoji']} Actualización de Pedido #{pedido.id}"
            html_content = render_to_string('emails/order_status_change.html', {
                'pedido': pedido,
                'cliente': pedido.cliente,
                'estado_anterior': estado_anterior,
                'estado_nuevo': pedido.get_estado_display(),
                'emoji': info['emoji'],
                'mensaje': info['mensaje']
            })
            return EmailService._send_html_email(
                subject, 
                html_content, 
                [pedido.cliente.email]
            )
        except Exception as e:
            logger.error(f"Error en send_order_status_change: {str(e)}")
            return False
    
    @staticmethod
    def send_reservation_confirmation(reserva):
        """
        Envía email de confirmación cuando se crea una reserva.
        """
        try:
            subject = f'✅ Confirmación de Reserva #{reserva.id} - Restaurante'
            html_content = render_to_string('emails/reservation_confirmation.html', {
                'reserva': reserva,
                'usuario': reserva.usuario
            })
            return EmailService._send_html_email(
                subject, 
                html_content, 
                [reserva.usuario.email]
            )
        except Exception as e:
            logger.error(f"Error en send_reservation_confirmation: {str(e)}")
            return False
    
    @staticmethod
    def send_reservation_status_change(reserva, estado_anterior):
        """
        Envía email cuando cambia el estado de una reserva.
        """
        try:
            # Mapeo de estados a emojis y mensajes
            estado_info = {
                'pendiente': {'emoji': '⏳', 'mensaje': 'Tu reserva está pendiente de confirmación'},
                'confirmada': {'emoji': '✅', 'mensaje': 'Tu reserva ha sido confirmada'},
                'cancelada': {'emoji': '❌', 'mensaje': 'Tu reserva ha sido cancelada'},
            }
            
            info = estado_info.get(reserva.estado, {'emoji': '📅', 'mensaje': 'Estado actualizado'})
            
            subject = f"{info['emoji']} Actualización de Reserva #{reserva.id}"
            html_content = render_to_string('emails/reservation_status_change.html', {
                'reserva': reserva,
                'usuario': reserva.usuario,
                'estado_anterior': estado_anterior,
                'estado_nuevo': reserva.get_estado_display(),
                'emoji': info['emoji'],
                'mensaje': info['mensaje']
            })
            return EmailService._send_html_email(
                subject, 
                html_content, 
                [reserva.usuario.email]
            )
        except Exception as e:
            logger.error(f"Error en send_reservation_status_change: {str(e)}")
            return False

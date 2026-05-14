from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def send_welcome_email(user):
        """Sends welcome email to a new user"""
        try:
            subject = 'Welcome to the Restaurant System'
            html_message = render_to_string('emails/welcome.html', {
                'nombre': user.nombre_completo,
                'user': user
            })
            from django.utils.html import strip_tags
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=True
            )
            logger.info(f"Welcome email sent to {user.email}")
        except Exception as e:
            logger.error(f"Error sending welcome email: {str(e)}")

    @staticmethod
    def send_order_confirmation(user, order):
        """Sends order confirmation email"""
        try:
            subject = f'Order Confirmation #{order.id}'
            html_message = render_to_string('emails/order_confirmation.html', {
                'user': user,
                'order': order,
                'items': order.items.all()
            })
            from django.utils.html import strip_tags
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=True
            )
            logger.info(f"Order confirmation email sent to {user.email}")
        except Exception as e:
            logger.error(f"Error sending order confirmation email: {str(e)}")
    
    @staticmethod
    def send_password_reset_email(user, request):
        """Envía email de recuperación de contraseña"""
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                f'/usuarios/reset/{uid}/{token}/'
            )
            
            subject = 'Recuperación de Contraseña'
            message = render_to_string('emails/password_reset.html', {
                'user': user,
                'reset_url': reset_url
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            logger.info(f'Email de recuperación enviado a {user.email}')
        except Exception as e:
            logger.error(f'Error enviando email de recuperación a {user.email}: {str(e)}')
    
    @staticmethod
    def send_account_activation_email(user):
        """Envía email de activación de cuenta"""
        try:
            subject = 'Cuenta Activada'
            message = render_to_string('emails/account_activated.html', {
                'user': user
            })
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            logger.info(f'Email de activación enviado a {user.email}')
        except Exception as e:
            logger.error(f'Error enviando email de activación a {user.email}: {str(e)}')
    
    @staticmethod
    def send_account_deactivation_email(user):
        """Envía email de desactivación de cuenta"""
        try:
            subject = 'Cuenta Desactivada'
            message = render_to_string('emails/account_deactivated.html', {
                'user': user
            })
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            logger.info(f'Email de desactivación enviado a {user.email}')
        except Exception as e:
            logger.error(f'Error enviando email de desactivación a {user.email}: {str(e)}')


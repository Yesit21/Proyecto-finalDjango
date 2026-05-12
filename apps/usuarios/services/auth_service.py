from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class AuthService:
    @staticmethod
    def send_welcome_email(user):
        subject = 'Bienvenido al Sistema de Restaurante'
        message = render_to_string('emails/welcome.html', {
            'user': user,
            'nombre': user.nombre_completo
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True
        )
    
    @staticmethod
    def send_password_reset_email(user, request):
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
            fail_silently=True
        )
    
    @staticmethod
    def send_account_activation_email(user):
        subject = 'Cuenta Activada'
        message = render_to_string('emails/account_activated.html', {
            'user': user
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True
        )
    
    @staticmethod
    def send_account_deactivation_email(user):
        subject = 'Cuenta Desactivada'
        message = render_to_string('emails/account_deactivated.html', {
            'user': user
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True
        )

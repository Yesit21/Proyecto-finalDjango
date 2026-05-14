from django.shortcuts import redirect
from django.urls import reverse


def home(request):
    """
    Vista principal que redirige según el estado de autenticación y rol del usuario.
    - No autenticado: redirige a login
    - Cliente: redirige al menú
    - Mesero/Administrador: redirige al dashboard
    """
    if not request.user.is_authenticated:
        return redirect(reverse("usuarios:login"))
    
    # Redirigir según el rol del usuario
    if request.user.rol == 'cliente':
        return redirect(reverse("menu:lista"))
    else:  # mesero o administrador
        return redirect(reverse("dashboard:home"))

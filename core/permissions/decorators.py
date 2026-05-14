from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('usuarios:login')
            if request.user.rol not in roles:
                messages.error(request, 'No tienes permisos')
                return redirect('dashboard:home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    return role_required(['administrador'])(view_func)

def mesero_required(view_func):
    return role_required(['mesero', 'administrador'])(view_func)

def cliente_required(view_func):
    return role_required(['cliente'])(view_func)

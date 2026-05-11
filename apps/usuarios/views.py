from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.permissions.base import AdminRequiredMixin
from core.permissions.decorators import admin_required
from .models import Usuario
from .forms import LoginForm, RegistroForm, UsuarioCreateForm, UsuarioUpdateForm
from .services.auth_service import AuthService
from .services.usuario_service import UsuarioService

def login_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.activo:
                    login(request, user)
                    
                    if not remember_me:
                        request.session.set_expiry(0)
                    
                    messages.success(request, f'Bienvenido {user.nombre_completo}')
                    
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('usuarios:perfil')
                else:
                    messages.error(request, 'Tu cuenta está desactivada')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = 'cliente'
            user.save()
            
            AuthService.send_welcome_email(user)
            
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('usuarios:perfil')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.info(request, f'Hasta pronto {username}')
    return redirect('usuarios:login')

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})

@login_required
@admin_required
def usuarios_lista(request):
    usuarios = UsuarioService.get_all_usuarios()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@login_required
@admin_required
def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.username} creado exitosamente')
            return redirect('usuarios:lista')
    else:
        form = UsuarioCreateForm()
    
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Crear Usuario'})

@login_required
@admin_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado')
            return redirect('usuarios:lista')
    else:
        form = UsuarioUpdateForm(instance=usuario)
    
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Editar Usuario', 'usuario': usuario})

@login_required
@admin_required
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.user.id == usuario.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta')
        return redirect('usuarios:lista')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado')
        return redirect('usuarios:lista')
    
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})

@login_required
@admin_required
def usuario_toggle_activo(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.user.id == usuario.id:
        messages.error(request, 'No puedes desactivar tu propia cuenta')
        return redirect('usuarios:lista')
    
    usuario.activo = not usuario.activo
    usuario.save()
    
    estado = 'activado' if usuario.activo else 'desactivado'
    messages.success(request, f'Usuario {usuario.username} {estado}')
    
    return redirect('usuarios:lista')

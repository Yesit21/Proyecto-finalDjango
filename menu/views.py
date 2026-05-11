from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plato, Categoria, Ingrediente
from .forms import PlatoForm, CategoriaForm, IngredienteForm

def menu_list(request):
    categorias = Categoria.objects.filter(activo=True)
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        platos = Plato.objects.filter(categoria_id=categoria_id, disponible=True)
    else:
        platos = Plato.objects.filter(disponible=True)
    return render(request, 'menu/lista.html', {'platos': platos, 'categorias': categorias})

def plato_detalle(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    return render(request, 'menu/detalle.html', {'plato': plato})

@login_required
def plato_crear(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('menu:lista')
    
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato creado')
            return redirect('menu:lista')
    else:
        form = PlatoForm()
    return render(request, 'menu/plato_form.html', {'form': form})

@login_required
def plato_editar(request, pk):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('menu:lista')
    
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato actualizado')
            return redirect('menu:detalle', pk=pk)
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'menu/plato_form.html', {'form': form, 'plato': plato})

@login_required
def plato_eliminar(request, pk):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('menu:lista')
    
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado')
        return redirect('menu:lista')
    return render(request, 'menu/plato_confirm_delete.html', {'plato': plato})

@login_required
def ingrediente_lista(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    ingredientes = Ingrediente.objects.all()
    return render(request, 'menu/ingrediente_lista.html', {'ingredientes': ingredientes})

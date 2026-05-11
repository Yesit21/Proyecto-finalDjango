from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MovimientoInventario, Proveedor, OrdenCompra
from menu.models import Ingrediente
from .forms import MovimientoInventarioForm, ProveedorForm, OrdenCompraForm

@login_required
def inventario_lista(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    ingredientes = Ingrediente.objects.all()
    return render(request, 'inventario/lista.html', {'ingredientes': ingredientes})

@login_required
def movimiento_crear(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            
            ingrediente = movimiento.ingrediente
            if movimiento.tipo == 'entrada':
                ingrediente.stock_actual += movimiento.cantidad
            elif movimiento.tipo == 'salida':
                ingrediente.stock_actual -= movimiento.cantidad
            else:
                ingrediente.stock_actual = movimiento.cantidad
            ingrediente.save()
            
            messages.success(request, 'Movimiento registrado')
            return redirect('inventario:lista')
    else:
        form = MovimientoInventarioForm()
    return render(request, 'inventario/movimiento_form.html', {'form': form})

@login_required
def movimientos_lista(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    movimientos = MovimientoInventario.objects.all()
    return render(request, 'inventario/movimientos.html', {'movimientos': movimientos})

@login_required
def proveedores_lista(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    proveedores = Proveedor.objects.all()
    return render(request, 'inventario/proveedores.html', {'proveedores': proveedores})

@login_required
def proveedor_crear(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado')
            return redirect('inventario:proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'inventario/proveedor_form.html', {'form': form})

@login_required
def ordenes_compra_lista(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    ordenes = OrdenCompra.objects.all()
    return render(request, 'inventario/ordenes.html', {'ordenes': ordenes})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MovimientoInventarioForm, ProductoForm
from .models import MovimientoInventario, Producto


@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    alertas = productos.filter(stock_actual__lte=F('alerta_stock'))
    return render(request, 'inventario/lista.html', {
        'productos': productos,
        'alertas': alertas,
    })


@login_required
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect('inventario:lista')
    return render(request, 'inventario/producto_form.html', {'form': form, 'titulo': 'Crear Producto'})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('inventario:lista')
    return render(request, 'inventario/producto_form.html', {'form': form, 'titulo': 'Editar Producto'})


@login_required
def crear_movimiento(request):
    form = MovimientoInventarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Movimiento de inventario registrado.')
        return redirect('inventario:historial')
    return render(request, 'inventario/movimiento_form.html', {'form': form})


@login_required
def historial_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related('producto').all()
    return render(request, 'inventario/movimientos.html', {'movimientos': movimientos})

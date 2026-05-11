from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Pedido, DetallePedido, Carrito, ItemCarrito
from menu.models import Plato

@login_required
def carrito_view(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'pedidos/carrito.html', {'carrito': carrito})

@login_required
def agregar_carrito(request, plato_id):
    plato = get_object_or_404(Plato, pk=plato_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, plato=plato)
    if not created:
        item.cantidad += 1
        item.save()
    messages.success(request, f'{plato.nombre} agregado al carrito')
    return redirect('pedidos:carrito')

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)
    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad > 0:
        item.cantidad = cantidad
        item.save()
    else:
        item.delete()
    return redirect('pedidos:carrito')

@login_required
def eliminar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Item eliminado del carrito')
    return redirect('pedidos:carrito')

@login_required
def crear_pedido(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    if not carrito.items.exists():
        messages.error(request, 'El carrito está vacío')
        return redirect('pedidos:carrito')
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo', 'local')
        mesa = request.POST.get('mesa')
        direccion = request.POST.get('direccion', '')
        
        pedido = Pedido.objects.create(
            cliente=request.user,
            tipo=tipo,
            mesa=mesa if mesa else None,
            direccion_entrega=direccion
        )
        
        for item in carrito.items.all():
            DetallePedido.objects.create(
                pedido=pedido,
                plato=item.plato,
                cantidad=item.cantidad,
                precio_unitario=item.plato.precio
            )
        
        pedido.calcular_total()
        carrito.items.all().delete()
        
        send_mail(
            'Confirmación de Pedido',
            f'Tu pedido #{pedido.id} ha sido recibido. Total: ${pedido.total}',
            'noreply@restaurante.com',
            [request.user.email],
        )
        
        messages.success(request, f'Pedido #{pedido.id} creado exitosamente')
        return redirect('pedidos:detalle', pk=pedido.id)
    
    return render(request, 'pedidos/crear_pedido.html', {'carrito': carrito})

@login_required
def pedido_detalle(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.cliente != request.user and request.user.rol not in ['mesero', 'administrador']:
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')
    return render(request, 'pedidos/mis_pedidos.html', {'pedidos': pedidos})

@login_required
def pedidos_lista(request):
    if request.user.rol not in ['mesero', 'administrador']:
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})

@login_required
def actualizar_estado_pedido(request, pk):
    if request.user.rol not in ['mesero', 'administrador']:
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard:home')
    
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        if not pedido.mesero:
            pedido.mesero = request.user
        pedido.save()
        messages.success(request, 'Estado actualizado')
    return redirect('pedidos:detalle', pk=pk)

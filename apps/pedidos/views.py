from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.inventario.models import Producto
from .forms import EstadoPedidoForm
from .models import Pedido, PedidoItem

CART_SESSION_KEY = 'pedidos_carrito'


def _get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


@login_required
def lista_pedidos(request):
    productos = Producto.objects.all().order_by('nombre')
    pedidos = Pedido.objects.filter(cliente=request.user) if not request.user.is_staff else Pedido.objects.all()
    return render(request, 'pedidos/lista.html', {
        'productos': productos,
        'pedidos': pedidos,
    })


@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    
    # Validar que el producto tenga stock disponible
    if producto.stock_actual <= 0:
        messages.error(request, f'{producto.nombre} no tiene stock disponible.')
        return redirect('pedidos:lista')
    
    cart = _get_cart(request)
    item = cart.get(str(producto.id), {
        'nombre': producto.nombre,
        'precio': str(producto.precio),
        'cantidad': 0,
    })
    
    # Validar que no se exceda el stock disponible
    nueva_cantidad = item['cantidad'] + 1
    if nueva_cantidad > producto.stock_actual:
        messages.warning(request, f'Solo hay {producto.stock_actual} unidades disponibles de {producto.nombre}.')
        return redirect('pedidos:carrito')
    
    item['cantidad'] = nueva_cantidad
    cart[str(producto.id)] = item
    _save_cart(request, cart)
    messages.success(request, f'Agregado {producto.nombre} al carrito.')
    return redirect('pedidos:carrito')


@login_required
def eliminar_carrito(request, producto_id):
    cart = _get_cart(request)
    cart.pop(str(producto_id), None)
    _save_cart(request, cart)
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('pedidos:carrito')


@login_required
def carrito(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0.00')
    for producto_id, item in cart.items():
        subtotal = Decimal(item['precio']) * item['cantidad']
        total += subtotal
        items.append({
            'producto_id': producto_id,
            'nombre': item['nombre'],
            'precio': Decimal(item['precio']),
            'cantidad': item['cantidad'],
            'subtotal': subtotal,
        })

    return render(request, 'pedidos/carrito.html', {
        'items': items,
        'total': total,
    })


@login_required
def realizar_pedido(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, 'El carrito está vacío.')
        return redirect('pedidos:carrito')

    # Validar stock antes de crear el pedido
    errores_stock = []
    for producto_id, item in cart.items():
        producto = Producto.objects.filter(pk=int(producto_id)).first()
        if producto:
            if producto.stock_actual < item['cantidad']:
                errores_stock.append(
                    f"{item['nombre']}: solo hay {producto.stock_actual} unidades disponibles (solicitaste {item['cantidad']})"
                )
    
    if errores_stock:
        for error in errores_stock:
            messages.error(request, error)
        return redirect('pedidos:carrito')

    # Crear el pedido
    pedido = Pedido.objects.create(cliente=request.user)
    total = Decimal('0.00')

    for producto_id, item in cart.items():
        producto = Producto.objects.filter(pk=int(producto_id)).first()
        cantidad = item['cantidad']
        precio = Decimal(item['precio'])
        subtotal = precio * cantidad

        PedidoItem.objects.create(
            pedido=pedido,
            producto=producto,
            nombre=item['nombre'],
            cantidad=cantidad,
            precio_unitario=precio,
        )

        # Descontar stock (ahora validado)
        if producto:
            producto.stock_actual -= cantidad
            producto.save(update_fields=['stock_actual'])

        total += subtotal

    pedido.total = total
    pedido.save(update_fields=['total'])
    request.session.pop(CART_SESSION_KEY, None)
    messages.success(request, f'Pedido #{pedido.id} realizado con éxito.')
    return redirect('pedidos:mis_pedidos')


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')
    return render(request, 'pedidos/mis_pedidos.html', {'pedidos': pedidos})


@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})


@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if pedido.estado not in ['entregado', 'cancelado']:
        pedido.estado = 'cancelado'
        pedido.save(update_fields=['estado'])
        messages.success(request, 'Pedido cancelado correctamente.')
    else:
        messages.warning(request, 'No se puede cancelar este pedido.')
    return redirect('pedidos:detalle', pedido_id=pedido.pk)


@login_required
def actualizar_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    form = EstadoPedidoForm(request.POST or None, instance=pedido)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estado del pedido actualizado.')
        return redirect('pedidos:detalle', pedido_id=pedido.pk)
    return render(request, 'pedidos/estado_form.html', {'form': form, 'pedido': pedido})

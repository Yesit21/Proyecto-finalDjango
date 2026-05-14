from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from apps.inventario.models import Producto
from apps.menu.models import Plato
from apps.reservas.models import Reserva, Mesa
from services.email.email_service import EmailService
from .forms import EstadoPedidoForm
from .models import Pedido, PedidoItem
import logging

logger = logging.getLogger(__name__)

CART_SESSION_KEY = 'pedidos_carrito'


def _get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def _can_manage_all_pedidos(user):
    return getattr(user, "rol", None) in {"mesero", "administrador"}


def _can_view_pedido(user, pedido):
    if _can_manage_all_pedidos(user):
        return True
    return pedido.cliente_id == user.id


@login_required
def lista_pedidos(request):
    # Show available dishes instead of products
    platos = Plato.objects.filter(disponible=True).order_by('categoria', 'nombre')
    pedidos = Pedido.objects.filter(cliente=request.user) if not request.user.is_staff else Pedido.objects.all()
    return render(request, 'pedidos/lista.html', {
        'platos': platos,
        'pedidos': pedidos,
    })


@login_required
def agregar_carrito(request, plato_id):
    plato = get_object_or_404(Plato, pk=plato_id)
    
    # Validate that the dish is available
    if not plato.disponible:
        messages.error(request, f'{plato.nombre} is not available at this moment.')
        return redirect('pedidos:lista')
    
    cart = _get_cart(request)
    item = cart.get(str(plato.id), {
        'nombre': plato.nombre,
        'precio': str(plato.precio),
        'cantidad': 0,
        'tipo': 'plato'  # Identify that it is a dish
    })
    
    item['cantidad'] += 1
    cart[str(plato.id)] = item
    _save_cart(request, cart)
    messages.success(request, f'Added {plato.nombre} to the cart.')
    return redirect('pedidos:carrito')


@login_required
def eliminar_carrito(request, item_id):
    cart = _get_cart(request)
    cart.pop(str(item_id), None)
    _save_cart(request, cart)
    messages.success(request, 'Product removed from the cart.')
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

    # Available tables for the cart
    mesas_disponibles = Mesa.objects.filter(activa=True, estado='disponible')

    return render(request, 'pedidos/carrito.html', {
        'items': items,
        'total': total,
        'mesas_disponibles': mesas_disponibles,
    })


@login_required
def pago_simulado(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, 'El carrito está vacío.')
        return redirect('pedidos:carrito')

    if request.method == 'POST':
        return realizar_pedido(request)

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

    return render(request, 'pedidos/pago.html', {'items': items, 'total': total})



@login_required
def realizar_pedido(request):
    if request.method != 'POST':
        return redirect('pedidos:carrito')
        
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, 'The cart is empty.')
        return redirect('pedidos:carrito')

    # Reservation data if included
    quiere_reserva = request.POST.get('quiere_reserva') == 'on'
    reserva_obj = None
    
    if quiere_reserva:
        fecha_reserva = request.POST.get('fecha_reserva')
        cantidad_personas = request.POST.get('cantidad_personas')
        mesa_id = request.POST.get('mesa_reserva')
        observaciones = request.POST.get('observaciones_reserva', '')
        
        if not fecha_reserva or not cantidad_personas:
            messages.error(request, 'You must complete the reservation data.')
            return redirect('pedidos:carrito')
            
        try:
            mesa_obj = None
            if mesa_id:
                mesa_obj = Mesa.objects.filter(pk=mesa_id, estado='disponible', activa=True).first()
            
            reserva_obj = Reserva.objects.create(
                usuario=request.user,
                fecha_reserva=fecha_reserva,
                cantidad_personas=int(cantidad_personas),
                mesa=mesa_obj,
                observaciones=observaciones,
                estado='pendiente'
            )
            
            # If the client selected a table, mark it as reserved
            if mesa_obj:
                mesa_obj.estado = 'reservada'
                mesa_obj.save()
                
            messages.info(request, 'Your table reservation request has been created.')
        except Exception as e:
            logger.error(f"Error creating reservation from order: {str(e)}")
            messages.error(request, 'There was an error creating the table reservation.')

    # Create the order
    pedido = Pedido.objects.create(
        cliente=request.user,
        reserva=reserva_obj
    )
    total = Decimal('0')

    for item_id, item in cart.items():
        cantidad = item['cantidad']
        precio = Decimal(item['precio'])
        subtotal = precio * cantidad

        # Create the order item
        pedido_item = PedidoItem.objects.create(
            pedido=pedido,
            nombre=item['nombre'],
            cantidad=cantidad,
            precio_unitario=precio,
        )
        
        # Link with the dish if it is a dish
        if item.get('tipo') == 'plato':
            plato = Plato.objects.filter(pk=int(item_id)).first()
            if plato:
                pedido_item.plato = plato
                pedido_item.save(update_fields=['plato'])

            total += subtotal

        for inv_id, requerido in requerimientos_ingredientes.items():
            Producto.objects.filter(pk=inv_id).update(stock_actual=F('stock_actual') - requerido)

        pedido.total = total
        pedido.save(update_fields=['total'])
    EmailService.send_order_confirmation(pedido)
    request.session.pop(CART_SESSION_KEY, None)
    
    # Send order confirmation email
    try:
        EmailService.send_order_confirmation(pedido)
        logger.info(f"Confirmation email sent for order #{pedido.id}")
    except Exception as e:
        logger.error(f"Error sending order confirmation email: {str(e)}")
        
    # If there was a reservation, send reservation email
    if reserva_obj:
        try:
            EmailService.send_reservation_confirmation(reserva_obj)
            logger.info(f"Confirmation email sent for reservation #{reserva_obj.id}")
        except Exception as e:
            logger.error(f"Error sending reservation confirmation email: {str(e)}")
    
    messages.success(request, f'Order #{pedido.id} placed successfully.')
    return redirect('pedidos:mis_pedidos')


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')
    return render(request, 'pedidos/mis_pedidos.html', {'pedidos': pedidos})


@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if not _can_view_pedido(request.user, pedido):
        raise PermissionDenied
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})


@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if not _can_view_pedido(request.user, pedido):
        raise PermissionDenied
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
    estado_anterior = pedido.get_estado_display()
    
    form = EstadoPedidoForm(request.POST or None, instance=pedido)
    if form.is_valid():
        # Guardar el estado anterior antes de actualizar
        estado_anterior_codigo = pedido.estado
        form.save()
        
        # Enviar email solo si el estado cambió
        if estado_anterior_codigo != pedido.estado:
            try:
                EmailService.send_order_status_change(pedido, estado_anterior)
                logger.info(f"Email de cambio de estado enviado para pedido #{pedido.id}")
            except Exception as e:
                logger.error(f"Error enviando email de cambio de estado: {str(e)}")
        
        messages.success(request, 'Estado del pedido actualizado.')
        return redirect('pedidos:detalle', pedido_id=pedido.pk)
    return render(request, 'pedidos/estado_form.html', {'form': form, 'pedido': pedido})

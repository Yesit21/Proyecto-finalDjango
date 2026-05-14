PEDIDO_PENDIENTE = 'pendiente'
PEDIDO_EN_PREPARACION = 'en_preparacion'
PEDIDO_LISTO = 'listo'
PEDIDO_ENTREGADO = 'entregado'
PEDIDO_CANCELADO = 'cancelado'

ESTADOS_PEDIDO = (
    (PEDIDO_PENDIENTE, 'Pendiente'),
    (PEDIDO_EN_PREPARACION, 'En Preparación'),
    (PEDIDO_LISTO, 'Listo'),
    (PEDIDO_ENTREGADO, 'Entregado'),
    (PEDIDO_CANCELADO, 'Cancelado'),
)

RESERVA_PENDIENTE = 'pendiente'
RESERVA_CONFIRMADA = 'confirmada'
RESERVA_CANCELADA = 'cancelada'
RESERVA_COMPLETADA = 'completada'

ESTADOS_RESERVA = (
    (RESERVA_PENDIENTE, 'Pendiente'),
    (RESERVA_CONFIRMADA, 'Confirmada'),
    (RESERVA_CANCELADA, 'Cancelada'),
    (RESERVA_COMPLETADA, 'Completada'),
)

MESA_DISPONIBLE = 'disponible'
MESA_OCUPADA = 'ocupada'
MESA_RESERVADA = 'reservada'
MESA_MANTENIMIENTO = 'mantenimiento'

ESTADOS_MESA = (
    (MESA_DISPONIBLE, 'Disponible'),
    (MESA_OCUPADA, 'Ocupada'),
    (MESA_RESERVADA, 'Reservada'),
    (MESA_MANTENIMIENTO, 'Mantenimiento'),
)

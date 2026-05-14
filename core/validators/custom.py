from django.core.exceptions import ValidationError
import re

def validate_phone(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError('Número de teléfono inválido')

def validate_positive(value):
    if value < 0:
        raise ValidationError('El valor debe ser positivo')

def validate_stock(value):
    if value < 0:
        raise ValidationError('El stock no puede ser negativo')

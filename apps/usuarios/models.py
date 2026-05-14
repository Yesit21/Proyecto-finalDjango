from django.contrib.auth.models import AbstractUser
from django.db import models
from core.constants.roles import ROLES, CLIENTE, MESERO, ADMINISTRADOR
from core.validators.custom import validate_phone

class Usuario(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROLES, default=CLIENTE, verbose_name="Rol")
    telefono = models.CharField(max_length=15, blank=True, validators=[validate_phone], verbose_name="Teléfono")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    foto = models.ImageField(upload_to='uploads/usuarios/', blank=True, null=True, verbose_name="Foto")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
    
    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def is_administrador(self):
        return self.rol == ADMINISTRADOR
    
    def is_mesero(self):
        return self.rol == MESERO
    
    def is_cliente(self):
        return self.rol == CLIENTE

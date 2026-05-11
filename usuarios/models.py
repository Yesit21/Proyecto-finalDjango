from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('mesero', 'Mesero'),
        ('administrador', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"

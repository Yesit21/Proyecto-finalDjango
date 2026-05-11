from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    telefono = models.CharField('Telefono', max_length=20, blank=True, null=True)
    direccion = models.CharField('Direccion', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

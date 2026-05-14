from django.db.models import Q, Count
from apps.usuarios.models import Usuario

class UsuarioService:
    @staticmethod
    def get_all_usuarios():
        return Usuario.objects.all().order_by('-fecha_creacion')
    
    @staticmethod
    def get_usuarios_activos():
        return Usuario.objects.filter(activo=True)
    
    @staticmethod
    def get_usuarios_por_rol(rol):
        return Usuario.objects.filter(rol=rol)
    
    @staticmethod
    def buscar_usuarios(query):
        return Usuario.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    @staticmethod
    def get_estadisticas_usuarios():
        return {
            'total': Usuario.objects.count(),
            'activos': Usuario.objects.filter(activo=True).count(),
            'inactivos': Usuario.objects.filter(activo=False).count(),
            'por_rol': Usuario.objects.values('rol').annotate(count=Count('id'))
        }
    
    @staticmethod
    def activar_usuario(usuario):
        usuario.activo = True
        usuario.save()
        return usuario
    
    @staticmethod
    def desactivar_usuario(usuario):
        usuario.activo = False
        usuario.save()
        return usuario

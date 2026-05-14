from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Usuario
from .forms import UsuarioAdminForm

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioAdminForm
    list_display = ['username', 'email', 'nombre_completo_display', 'rol_badge', 'activo_badge', 'fecha_creacion']
    list_filter = ['rol', 'activo', 'is_staff', 'is_superuser', 'fecha_creacion']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telefono']
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información de Acceso', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'telefono', 'direccion', 'foto')
        }),
        ('Rol y Permisos', {
            'fields': ('rol', 'activo', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Información de Acceso', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'telefono')
        }),
        ('Rol', {
            'fields': ('rol', 'activo')
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'last_login', 'date_joined']
    
    def nombre_completo_display(self, obj):
        return obj.nombre_completo
    nombre_completo_display.short_description = 'Nombre Completo'
    
    def rol_badge(self, obj):
        colors = {
            'administrador': '#dc2626',
            'mesero': '#2563eb',
            'cliente': '#16a34a'
        }
        color = colors.get(obj.rol, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_rol_display()
        )
    rol_badge.short_description = 'Rol'
    
    def activo_badge(self, obj):
        color = '#16a34a' if obj.activo else '#dc2626'
        texto = '✓ Activo' if obj.activo else '✗ Inactivo'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            texto
        )
    activo_badge.short_description = 'Estado'
    
    actions = ['activar_usuarios', 'desactivar_usuarios']
    
    def activar_usuarios(self, request, queryset):
        count = queryset.update(activo=True)
        self.message_user(request, f'{count} usuario(s) activado(s)')
    activar_usuarios.short_description = 'Activar usuarios seleccionados'
    
    def desactivar_usuarios(self, request, queryset):
        count = queryset.update(activo=False)
        self.message_user(request, f'{count} usuario(s) desactivado(s)')
    desactivar_usuarios.short_description = 'Desactivar usuarios seleccionados'

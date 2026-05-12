# 🚨 ACCIONES DE SEGURIDAD URGENTES

## ⚠️ IMPORTANTE: Ejecutar INMEDIATAMENTE

### 1. Cambiar Contraseña de Aplicación de Gmail

Tu contraseña de aplicación actual está expuesta en el archivo `.env`:
- Email: `marlonchamoro21@gmail.com`
- Contraseña: `axep pwof oiux vohj`

**PASOS:**
1. Ve a https://myaccount.google.com/apppasswords
2. Revoca la contraseña actual `axep pwof oiux vohj`
3. Genera una nueva contraseña de aplicación
4. Actualiza el archivo `.env` con la nueva contraseña

### 2. Generar Nueva SECRET_KEY

La SECRET_KEY actual es insegura y está expuesta.

**PASOS:**
1. Abre una terminal Python:
```bash
python manage.py shell
```

2. Ejecuta:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

3. Copia la nueva clave generada
4. Actualiza el archivo `.env`:
```
SECRET_KEY=tu-nueva-clave-aqui
```

### 3. Verificar que .env NO esté en Git

✅ **BUENA NOTICIA:** Ya está en `.gitignore`

Pero verifica que no se haya commiteado antes:
```bash
git log --all --full-history -- .env
```

Si aparece en el historial, considera:
- Cambiar todas las credenciales
- Limpiar el historial de Git (avanzado)

### 4. Configuración para Producción

Cuando despliegues a producción, actualiza `restaurante_project/settings.py`:

```python
DEBUG = False  # ⚠️ NUNCA True en producción

ALLOWED_HOSTS = [
    'tu-dominio.com',
    'www.tu-dominio.com',
    # NO uses '*'
]
```

---

## ✅ Correcciones Aplicadas

### Errores de Código Corregidos:
- ✅ `item.plato.nombre` → `item.nombre` en pdf_service.py
- ✅ `reserva.cliente.email` → `reserva.usuario.email` en email_service.py
- ✅ Validación de stock en carrito y pedidos
- ✅ Validación de fechas en formulario de reservas
- ✅ Manejo de errores en envío de emails (con logging)
- ✅ Eliminado `@apply` de Tailwind en navbar

### Mejoras de Seguridad:
- ✅ Validación de stock antes de agregar al carrito
- ✅ Validación de stock antes de realizar pedido
- ✅ Mensajes de error específicos para el usuario
- ✅ Logging de errores de email
- ✅ `fail_silently=False` para detectar problemas

---

## 📋 Próximos Pasos Recomendados

### Corto Plazo (Esta Semana):
1. [ ] Decidir qué archivo de settings usar (eliminar el duplicado)
2. [ ] Configurar o remover Redis (está instalado pero no usado)
3. [ ] Agregar paginación en listas de productos y pedidos
4. [ ] Probar todas las funcionalidades después de los cambios

### Mediano Plazo (Este Mes):
1. [ ] Migrar a PostgreSQL para producción
2. [ ] Configurar logging estructurado
3. [ ] Agregar tests unitarios
4. [ ] Configurar Tailwind correctamente (si lo necesitas)

---

## 🔍 Archivos Modificados

1. `templates/components/navbar/main.html` - Eliminado @apply, agregadas URLs reales
2. `services/email/email_service.py` - Corregido campo reserva.usuario
3. `services/reports/pdf_service.py` - Corregido campo item.nombre
4. `apps/pedidos/views.py` - Agregada validación de stock
5. `apps/reservas/forms.py` - Agregada validación de fechas
6. `apps/usuarios/services/auth_service.py` - Mejorado manejo de errores

---

## 📞 Soporte

Si tienes dudas sobre alguna de estas correcciones, pregunta antes de continuar.

**RECUERDA:** La seguridad es lo primero. Cambia las credenciales HOY.

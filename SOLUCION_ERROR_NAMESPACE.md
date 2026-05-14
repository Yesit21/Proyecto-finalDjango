# 🔧 Solución al Error: 'reservas' is not a registered namespace

## 📋 Descripción del Error

```
NoReverseMatch at /usuarios/login/
'reservas' is not a registered namespace
```

Este error ocurre cuando Django no puede encontrar el namespace 'reservas' en las URLs.

---

## 🎯 Causa del Problema

Tu compañero está usando un archivo de configuración diferente:
- **Archivo usado:** `config.settings.development`
- **Archivo correcto:** `restaurante_project.settings`

---

## ✅ Solución 1: Cambiar el Archivo de Settings (RECOMENDADO)

### Opción A: Cambiar Variable de Entorno

1. **Busca dónde se define `DJANGO_SETTINGS_MODULE`**

   Puede estar en:
   - Variables de entorno del sistema
   - Archivo `.env`
   - Configuración de VS Code (launch.json)
   - manage.py

2. **Cambia el valor a:**
   ```
   DJANGO_SETTINGS_MODULE=restaurante_project.settings
   ```

### Opción B: Modificar manage.py

Si el archivo `manage.py` tiene esta línea:
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
```

Cámbiala a:
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante_project.settings')
```

### Opción C: Ejecutar con el Settings Correcto

```bash
python manage.py runserver --settings=restaurante_project.settings
```

---

## ✅ Solución 2: Verificar que Tenga los Últimos Cambios

Tu compañero debe hacer pull de los últimos cambios:

```bash
git pull origin main
```

Los cambios incluyen:
- ✅ Footer corregido con validación de usuario autenticado
- ✅ Correcciones de errores críticos
- ✅ Validaciones de stock y reservas

---

## ✅ Solución 3: Verificar Estructura de URLs

Asegúrate de que el archivo `restaurante_project/urls.py` tenga:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/usuarios/login/', permanent=False)),
    path('usuarios/', include('apps.usuarios.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('menu/', include('apps.menu.urls')),
    path('reservas/', include('apps.reservas.urls')),  # ← Debe estar aquí
    path('reportes-api/', include('apps.reportes.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]
```

Y que `apps/reservas/urls.py` tenga:

```python
from django.urls import path
from . import views

app_name = 'reservas'  # ← Debe tener este namespace

urlpatterns = [
    path('crear/', views.CrearReservaView.as_view(), name='crear'),
    path('lista/', views.ListaReservasView.as_view(), name='lista'),
    # ... más rutas
]
```

---

## 🔍 Verificación

Después de aplicar la solución, verifica con:

```bash
python manage.py check
python manage.py show_urls  # Si tienes django-extensions
```

O simplemente intenta acceder a:
```
http://127.0.0.1:8000/usuarios/login/
```

---

## 📝 Pasos Completos para tu Compañero

1. **Hacer pull de los últimos cambios:**
   ```bash
   git pull origin main
   ```

2. **Verificar el archivo de settings usado:**
   ```bash
   # En Windows
   echo %DJANGO_SETTINGS_MODULE%
   
   # O revisar manage.py
   ```

3. **Cambiar a restaurante_project.settings** (ver opciones arriba)

4. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

6. **Probar en el navegador:**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🚨 Si el Error Persiste

### Verificar que todas las apps estén en INSTALLED_APPS

En el archivo de settings que esté usando, debe tener:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.usuarios',
    'apps.menu',
    'apps.pedidos',
    'apps.reservas',  # ← Debe estar aquí
    'apps.inventario',
    'apps.dashboard',
    
    'core',
]
```

### Limpiar Cache de Python

```bash
# Eliminar archivos .pyc
find . -type f -name "*.pyc" -delete
# O en Windows
del /s /q *.pyc

# Eliminar carpetas __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +
# O en Windows
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

---

## 📞 Contacto

Si después de seguir estos pasos el error persiste, comparte:
1. El contenido de `manage.py`
2. El valor de `DJANGO_SETTINGS_MODULE`
3. El contenido de `restaurante_project/urls.py`
4. La salida de `python manage.py check`

---

## ✅ Cambios Aplicados en el Último Commit

He corregido el footer para que no cause errores cuando el usuario no está autenticado:

**Antes:**
```html
<li><a href="{% url 'menu:lista' %}">Menú</a></li>
<li><a href="{% url 'reservas:crear' %}">Reservas</a></li>
```

**Ahora:**
```html
{% if user.is_authenticated %}
    <li><a href="{% url 'menu:lista' %}">Menú</a></li>
    <li><a href="{% url 'reservas:crear' %}">Reservas</a></li>
{% else %}
    <li><a href="{% url 'usuarios:login' %}">Iniciar Sesión</a></li>
    <li><a href="{% url 'usuarios:registro' %}">Registrarse</a></li>
{% endif %}
```

Esto evita que se intenten resolver URLs que requieren autenticación cuando el usuario no está logueado.

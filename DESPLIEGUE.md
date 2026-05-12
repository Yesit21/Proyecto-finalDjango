# 🚀 Guía de Despliegue - Sistema de Gestión de Restaurante

Esta guía te ayudará a desplegar tu aplicación Django en diferentes plataformas.

---

## 📋 Tabla de Contenidos

- [Preparación](#-preparación)
- [Opción 1: PythonAnywhere](#-opción-1-pythonanywhere-con-sqlite)
- [Opción 2: Render](#-opción-2-render-con-postgresql)
- [Opción 3: Railway](#-opción-3-railway-con-postgresql)
- [Configuración Post-Despliegue](#-configuración-post-despliegue)
- [Solución de Problemas](#-solución-de-problemas)

---

## 🔧 Preparación

Antes de desplegar, asegúrate de tener:

### 1. Archivos Necesarios

✅ `requirements.txt` - Dependencias del proyecto  
✅ `.env.example` - Ejemplo de variables de entorno  
✅ `README.md` - Documentación  
✅ `.gitignore` - Archivos a ignorar  

### 2. Configuración de Settings

Crea un archivo `restaurante_project/settings_production.py`:

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static Files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 3. Actualizar requirements.txt

Agrega estas dependencias para producción:

```txt
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9  # Solo si usas PostgreSQL
dj-database-url==2.1.0
```

---

## 🐍 Opción 1: PythonAnywhere (Con SQLite)

**Ventajas:**
- ✅ Gratis para siempre
- ✅ Usa SQLite (no necesitas cambiar nada)
- ✅ Fácil de configurar
- ✅ Ideal para proyectos académicos

**Desventajas:**
- ⚠️ Limitado a 512MB de almacenamiento
- ⚠️ Dominio: `tu-usuario.pythonanywhere.com`

### Paso 1: Crear Cuenta

1. Ve a [PythonAnywhere](https://www.pythonanywhere.com/)
2. Crea una cuenta gratuita
3. Verifica tu email

### Paso 2: Subir el Código

**Opción A: Desde GitHub (Recomendado)**

```bash
# En la consola de PythonAnywhere
cd ~
git clone https://github.com/Yesit21/Proyecto-finalDjango.git
cd Proyecto-finalDjango
```

**Opción B: Subir archivos manualmente**

1. Ve a la pestaña "Files"
2. Sube tu proyecto en formato ZIP
3. Descomprime el archivo

### Paso 3: Crear Entorno Virtual

```bash
mkvirtualenv --python=/usr/bin/python3.10 restaurante-env
workon restaurante-env
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Crea un archivo `.env`:

```bash
nano .env
```

Agrega:

```env
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=False
ALLOWED_HOSTS=tu-usuario.pythonanywhere.com
```

### Paso 5: Aplicar Migraciones

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Paso 6: Configurar Web App

1. Ve a la pestaña "Web"
2. Click en "Add a new web app"
3. Selecciona "Manual configuration"
4. Selecciona Python 3.10

### Paso 7: Configurar WSGI

Edita el archivo WSGI:

```python
import os
import sys

# Ruta a tu proyecto
path = '/home/tu-usuario/Proyecto-finalDjango'
if path not in sys.path:
    sys.path.append(path)

# Variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurante_project.settings'

# Cargar .env
from dotenv import load_dotenv
project_folder = os.path.expanduser(path)
load_dotenv(os.path.join(project_folder, '.env'))

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Paso 8: Configurar Archivos Estáticos

En la pestaña "Web", configura:

- **Static files:**
  - URL: `/static/`
  - Directory: `/home/tu-usuario/Proyecto-finalDjango/static/`

- **Media files:**
  - URL: `/media/`
  - Directory: `/home/tu-usuario/Proyecto-finalDjango/media/`

### Paso 9: Recargar la Aplicación

Click en el botón verde "Reload" en la pestaña Web.

### Paso 10: Verificar

Visita: `https://tu-usuario.pythonanywhere.com`

---

## 🎨 Opción 2: Render (Con PostgreSQL)

**Ventajas:**
- ✅ Gratis con PostgreSQL
- ✅ Despliegue automático desde GitHub
- ✅ SSL gratis
- ✅ Más profesional

**Desventajas:**
- ⚠️ Requiere configurar PostgreSQL
- ⚠️ Se duerme después de 15 min de inactividad (plan gratuito)

### Paso 1: Preparar el Proyecto

1. **Crear `build.sh`:**

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

2. **Hacer ejecutable:**

```bash
chmod +x build.sh
```

3. **Actualizar `settings.py`:**

```python
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Whitenoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Paso 2: Crear Cuenta en Render

1. Ve a [Render](https://render.com/)
2. Regístrate con GitHub
3. Autoriza el acceso a tu repositorio

### Paso 3: Crear PostgreSQL Database

1. Click en "New +"
2. Selecciona "PostgreSQL"
3. Nombre: `restaurante-db`
4. Plan: Free
5. Click "Create Database"
6. **Copia la "Internal Database URL"**

### Paso 4: Crear Web Service

1. Click en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio
4. Configuración:
   - **Name:** `restaurante-app`
   - **Environment:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn restaurante_project.wsgi:application`

### Paso 5: Configurar Variables de Entorno

En "Environment", agrega:

```
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=False
DATABASE_URL=postgresql://... (la URL que copiaste)
ALLOWED_HOSTS=restaurante-app.onrender.com
PYTHON_VERSION=3.10.0
```

### Paso 6: Desplegar

1. Click "Create Web Service"
2. Espera 5-10 minutos
3. Visita tu URL: `https://restaurante-app.onrender.com`

### Paso 7: Crear Superusuario

En la consola de Render:

```bash
python manage.py createsuperuser
```

---

## 🚂 Opción 3: Railway (Con PostgreSQL)

**Ventajas:**
- ✅ Muy fácil de usar
- ✅ Despliegue automático
- ✅ PostgreSQL incluido
- ✅ $5 de crédito gratis

**Desventajas:**
- ⚠️ Requiere tarjeta de crédito (no cobra si no excedes el crédito)

### Paso 1: Crear Cuenta

1. Ve a [Railway](https://railway.app/)
2. Regístrate con GitHub
3. Verifica tu cuenta

### Paso 2: Crear Proyecto

1. Click "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Selecciona tu repositorio

### Paso 3: Agregar PostgreSQL

1. Click "New"
2. Selecciona "Database"
3. Selecciona "PostgreSQL"
4. Railway creará automáticamente la variable `DATABASE_URL`

### Paso 4: Configurar Variables de Entorno

En "Variables", agrega:

```
SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
PYTHON_VERSION=3.10.0
```

### Paso 5: Configurar Build

Crea `railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn restaurante_project.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Paso 6: Desplegar

Railway desplegará automáticamente. Visita tu URL en "Settings" → "Domains".

---

## ⚙️ Configuración Post-Despliegue

### 1. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 2. Cargar Datos Iniciales (Opcional)

```bash
python manage.py loaddata initial_data.json
```

### 3. Configurar Email

Actualiza las variables de entorno:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

### 4. Configurar Dominio Personalizado (Opcional)

En tu plataforma de despliegue, agrega tu dominio personalizado.

---

## 🔍 Solución de Problemas

### Error: "DisallowedHost"

**Solución:** Agrega tu dominio a `ALLOWED_HOSTS` en settings.

```python
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
```

### Error: "Static files not found"

**Solución:** Ejecuta `collectstatic`:

```bash
python manage.py collectstatic --noinput
```

### Error: "Database connection failed"

**Solución:** Verifica la variable `DATABASE_URL` en las variables de entorno.

### Error: "Module not found"

**Solución:** Verifica que todas las dependencias estén en `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### La aplicación es muy lenta

**Solución:** 
- En Render/Railway (plan gratuito), la app se duerme después de inactividad
- Considera actualizar al plan de pago
- Usa PythonAnywhere si necesitas que esté siempre activa

---

## 📊 Checklist de Despliegue

Antes de desplegar, verifica:

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` segura y en variable de entorno
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Todas las dependencias en `requirements.txt`
- [ ] Migraciones aplicadas
- [ ] Archivos estáticos recolectados
- [ ] Superusuario creado
- [ ] Variables de entorno configuradas
- [ ] SSL habilitado
- [ ] Emails configurados (opcional)

---

## 🎉 ¡Listo!

Tu aplicación debería estar funcionando en producción. 

**URLs de ejemplo:**
- PythonAnywhere: `https://tu-usuario.pythonanywhere.com`
- Render: `https://restaurante-app.onrender.com`
- Railway: `https://restaurante-app.up.railway.app`

---

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs de tu plataforma
2. Consulta la documentación oficial
3. Abre un issue en GitHub

**¡Buena suerte con tu despliegue!** 🚀


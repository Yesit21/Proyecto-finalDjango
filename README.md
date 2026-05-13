# 🍽️ Sistema de Gestión de Restaurante

![Django](https://img.shields.io/badge/Django-5.0.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.14.3-blue.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema web completo para la gestión integral de un restaurante, desarrollado con Django. Incluye gestión de pedidos, reservas, inventario, reportes y notificaciones automáticas por email.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías-utilizadas)
- [Requisitos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Funcionalidades](#-funcionalidades-principales)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Credenciales de Prueba](#-credenciales-de-prueba)
- [Despliegue](#-despliegue)
- [Autores](#-autores)
- [Licencia](#-licencia)

---

## ✨ Características

- 🔐 **Sistema de autenticación** con roles (Cliente, Mesero, Administrador)
- 🍕 **Gestión de menú** con categorías y precios
- 🛒 **Carrito de compras** y sistema de pedidos
- 📅 **Sistema de reservas** de mesas
- 📦 **Control de inventario** con alertas de stock bajo
- 📊 **Dashboard interactivo** con gráficos en tiempo real
- 📄 **Reportes exportables** en PDF y Excel
- 📧 **Notificaciones automáticas** por email
- 🎨 **Interfaz moderna** y responsive con modo oscuro/claro
- 📱 **Diseño responsive** para móviles y tablets

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 5.0.2** - Framework web de Python
- **Python 3.14.3** - Lenguaje de programación
- **SQLite3** - Base de datos
- **ReportLab** - Generación de PDFs
- **OpenPyXL** - Generación de archivos Excel

### Frontend
- **TailwindCSS** - Framework CSS
- **Alpine.js** - Framework JavaScript ligero
- **Chart.js** - Gráficos interactivos
- **Phosphor Icons** - Iconos modernos

### Otros
- **Django Email** - Sistema de emails
- **Python Decouple** - Gestión de variables de entorno
- **Git/GitHub** - Control de versiones

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10+** ([Descargar](https://www.python.org/downloads/))
- **pip** (gestor de paquetes de Python)
- **Git** ([Descargar](https://git-scm.com/downloads))
- **Navegador web moderno** (Chrome, Firefox, Edge)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yesit21/Proyecto-finalDjango.git
cd Proyecto-finalDjango
```

### 2. Crear entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu cuenta de administrador.

### 7. Compilar CSS de Tailwind (Opcional)

```bash
python manage.py tailwind build
```

### 8. Ejecutar el servidor

```bash
python manage.py runserver
```

Abre tu navegador en: **http://127.0.0.1:8000/**

---

## ⚙️ Configuración

### Configuración de Email

Para habilitar el envío de emails automáticos:

1. **Obtener App Password de Gmail:**
   - Ve a: https://myaccount.google.com/apppasswords
   - Crea una contraseña de aplicación
   - Copia la contraseña generada

2. **Actualizar `.env`:**
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=tu_app_password_aqui
   ```

3. **Reiniciar el servidor**

### Configuración de Tailwind

Si deseas personalizar los estilos:

1. Edita `tailwind.config.js`
2. Ejecuta: `python manage.py tailwind build`
3. Reinicia el servidor

---

## 📖 Uso

### Roles de Usuario

El sistema tiene 3 roles principales:

#### 👤 Cliente
- Ver menú de platos
- Agregar items al carrito
- Realizar pedidos
- Crear y gestionar reservas
- Ver historial de pedidos

#### 👨‍🍳 Mesero
- Todas las funciones de Cliente
- Acceso al Dashboard
- Actualizar estado de pedidos
- Ver reportes de pedidos y ventas
- Gestionar reservas

#### 👨‍💼 Administrador
- Todas las funciones de Mesero
- Gestión completa de usuarios
- Gestión de inventario
- Acceso a todos los reportes
- Exportar reportes en PDF/Excel
- Configuración del sistema

### Flujo de Trabajo

1. **Cliente realiza un pedido:**
   - Navega por el menú
   - Agrega platos al carrito
   - Confirma el pedido
   - Recibe email de confirmación

2. **Mesero procesa el pedido:**
   - Ve el pedido en el dashboard
   - Actualiza el estado (En preparación → Listo → Entregado)
   - Cliente recibe notificaciones por email

3. **Administrador genera reportes:**
   - Accede a "Exportar Reportes"
   - Selecciona tipo de reporte
   - Aplica filtros
   - Descarga en PDF o Excel

---

## 📁 Estructura del Proyecto

```
Proyecto-finalDjango/
├── apps/
│   ├── dashboard/          # Dashboard con gráficos
│   ├── inventario/         # Gestión de inventario
│   ├── menu/               # Gestión de platos
│   ├── pedidos/            # Sistema de pedidos
│   ├── reservas/           # Sistema de reservas
│   └── usuarios/           # Autenticación y usuarios
├── services/
│   ├── email/              # Servicio de emails
│   └── reports/            # Generación de reportes
├── templates/
│   ├── base/               # Templates base
│   ├── components/         # Componentes reutilizables
│   ├── dashboard/          # Templates del dashboard
│   ├── emails/             # Templates de emails
│   ├── menu/               # Templates del menú
│   ├── pedidos/            # Templates de pedidos
│   ├── reservas/           # Templates de reservas
│   └── usuarios/           # Templates de usuarios
├── static/
│   ├── css/                # Archivos CSS
│   ├── js/                 # Archivos JavaScript
│   └── images/             # Imágenes
├── restaurante_project/    # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI para despliegue
├── manage.py               # Script de gestión de Django
├── requirements.txt        # Dependencias del proyecto
├── .env.example            # Ejemplo de variables de entorno
└── README.md               # Este archivo
```

---

## 🎯 Funcionalidades Principales

### 1. Sistema de Autenticación
- Registro de usuarios con validación
- Login/Logout seguro
- Recuperación de contraseña
- Gestión de permisos por rol

### 2. Gestión de Menú
- CRUD completo de platos
- Categorías de platos
- Imágenes de platos
- Precios y descripciones

### 3. Sistema de Pedidos
- Carrito de compras interactivo
- Validación de stock en tiempo real
- Estados de pedido (Pendiente, En preparación, Listo, Entregado, Cancelado)
- Historial de pedidos por usuario
- Actualización automática de inventario

### 4. Sistema de Reservas
- Crear reservas con fecha y hora
- Validación de fechas futuras
- Estados de reserva (Pendiente, Confirmada, Cancelada)
- Gestión de cantidad de personas
- Observaciones personalizadas

### 5. Control de Inventario
- CRUD de productos
- Alertas de stock bajo
- Actualización automática al realizar pedidos
- Reportes de inventario

### 6. Dashboard Interactivo
- Gráficos en tiempo real con Chart.js
- Métricas de ventas e ingresos
- Pedidos por estado
- Platos más vendidos
- Productos con stock bajo

### 7. Sistema de Reportes
- **Reporte de Pedidos**: Lista detallada con filtros
- **Reporte de Ventas**: Métricas y top 10 platos
- **Reporte de Inventario**: Estado actual y alertas
- **Reporte de Reservas**: Lista con filtros
- Exportación en PDF y Excel
- Filtros por fecha, estado, categoría

### 8. Notificaciones por Email
- Confirmación de pedido
- Cambio de estado de pedido
- Confirmación de reserva
- Cambio de estado de reserva
- Templates HTML profesionales

---

## 📸 Capturas de Pantalla

### Página de Inicio
![Inicio](docs/screenshots/home.png)

### Menú de Platos
![Menú](docs/screenshots/menu.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Carrito de Compras
![Carrito](docs/screenshots/cart.png)

### Reportes
![Reportes](docs/screenshots/reports.png)

---

## 🔑 Credenciales de Prueba

Para probar el sistema, puedes usar estas credenciales:

### Administrador
```
Usuario: admin
Contraseña: admin123
```

### Mesero
```
Usuario: mesero
Contraseña: mesero123
```

### Cliente
```
Usuario: cliente
Contraseña: cliente123
```

**Nota:** Crea estos usuarios con el comando `createsuperuser` o desde el panel de administración.

---

## 🌐 Despliegue

### Preparación para Producción

#### 1. Configurar Settings para Producción

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

#### 2. Configurar Archivos Estáticos

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

```bash
python manage.py collectstatic --noinput
```

### Opción 1: PythonAnywhere (Recomendado para SQLite)

**Ventajas**:
- ✅ Gratis para siempre
- ✅ Usa SQLite (sin cambios necesarios)
- ✅ Fácil configuración
- ✅ Ideal para proyectos académicos

**Pasos**:

1. **Crear cuenta** en [PythonAnywhere](https://www.pythonanywhere.com/)

2. **Subir código**:
```bash
git clone https://github.com/Yesit21/Proyecto-finalDjango.git
cd Proyecto-finalDjango
```

3. **Crear entorno virtual**:
```bash
mkvirtualenv --python=/usr/bin/python3.10 restaurante-env
pip install -r requirements.txt
```

4. **Aplicar migraciones**:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

5. **Configurar Web App**:
   - Ir a pestaña "Web"
   - Crear nueva web app
   - Seleccionar "Manual configuration"
   - Python 3.10

6. **Configurar WSGI**:
```python
import os
import sys

path = '/home/tu-usuario/Proyecto-finalDjango'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurante_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

7. **Configurar archivos estáticos**:
   - URL: `/static/`
   - Directory: `/home/tu-usuario/Proyecto-finalDjango/static/`

8. **Recargar** la aplicación

### Opción 2: Render (Con PostgreSQL)

**Ventajas**:
- ✅ Gratis con PostgreSQL
- ✅ Despliegue automático desde GitHub
- ✅ SSL gratis
- ✅ Más profesional

**Pasos**:

1. **Preparar proyecto**:

Crear `build.sh`:
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

2. **Actualizar settings.py**:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

3. **Crear cuenta** en [Render](https://render.com/)

4. **Crear PostgreSQL Database**:
   - New → PostgreSQL
   - Plan: Free
   - Copiar "Internal Database URL"

5. **Crear Web Service**:
   - New → Web Service
   - Conectar repositorio
   - Build Command: `./build.sh`
   - Start Command: `gunicorn restaurante_project.wsgi:application`

6. **Variables de entorno**:
```
SECRET_KEY=tu-clave-secreta
DEBUG=False
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=tu-app.onrender.com
```

7. **Desplegar** (automático)

### Opción 3: Railway (Con PostgreSQL)

**Ventajas**:
- ✅ Muy fácil de usar
- ✅ PostgreSQL incluido
- ✅ $5 crédito gratis

**Pasos**:

1. **Crear cuenta** en [Railway](https://railway.app/)

2. **Crear proyecto**:
   - New Project
   - Deploy from GitHub repo

3. **Agregar PostgreSQL**:
   - New → Database → PostgreSQL

4. **Variables de entorno**:
```
SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
```

5. **Crear railway.json**:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn restaurante_project.wsgi:application"
  }
}
```

6. **Desplegar** (automático)

### Checklist de Despliegue

Antes de desplegar, verifica:

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` segura y en variable de entorno
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Dependencias en `requirements.txt`
- [ ] Migraciones aplicadas
- [ ] Archivos estáticos recolectados
- [ ] Superusuario creado
- [ ] Variables de entorno configuradas
- [ ] SSL habilitado
- [ ] Emails configurados

---

## 📊 Métricas del Proyecto

### Estadísticas de Código

```
Lenguaje          Archivos    Líneas    Código    Comentarios
─────────────────────────────────────────────────────────────
Python               45       5,000     4,200        800
HTML                 40       3,500     3,200        300
JavaScript            5         500       450         50
CSS                   3         300       280         20
─────────────────────────────────────────────────────────────
Total               93       9,300     8,130      1,170
```

### Funcionalidades Implementadas

- ✅ **6 Modelos** principales con relaciones
- ✅ **60+ URLs** configuradas
- ✅ **40+ Templates** HTML
- ✅ **15+ Formularios** validados
- ✅ **4 Tipos de reportes** (PDF + Excel)
- ✅ **4 Tipos de emails** automáticos
- ✅ **3 Roles** de usuario
- ✅ **8 Gráficos** interactivos

### Cobertura de Requisitos

| Requisito | Estado | Completitud |
|-----------|--------|-------------|
| Autenticación y autorización | ✅ | 100% |
| Modelado de datos (4+ modelos) | ✅ | 100% |
| Operaciones CRUD | ✅ | 100% |
| Panel de administración | ✅ | 100% |
| Reportes y exportación | ✅ | 100% |
| Interfaz responsive | ✅ | 100% |
| Validaciones y errores | ✅ | 100% |
| Despliegue | ⏳ | Pendiente |
| Documentación técnica | ✅ | 100% |
| Gráficos estadísticos | ✅ | 100% |

---

## 🔒 Seguridad

### Medidas Implementadas

#### 1. Autenticación
- ✅ Contraseñas hasheadas con PBKDF2
- ✅ Validación de contraseñas robustas
- ✅ Protección contra fuerza bruta
- ✅ Sesiones seguras

#### 2. Autorización
- ✅ Control de acceso por rol
- ✅ Decoradores `@login_required`
- ✅ Mixins de permisos
- ✅ Validación de permisos en vistas

#### 3. Protección CSRF
```python
# Todas las formas incluyen
{% csrf_token %}
```

#### 4. Validación de Datos
- ✅ Validación en formularios
- ✅ Validación en modelos
- ✅ Sanitización de inputs
- ✅ Prevención de SQL Injection (ORM)

#### 5. Configuración Segura
```python
# settings.py
SECRET_KEY = env('SECRET_KEY')  # En variable de entorno
DEBUG = False  # En producción
ALLOWED_HOSTS = ['dominio-especifico.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Recomendaciones de Seguridad

1. **Nunca** commitear el archivo `.env`
2. **Usar** contraseñas de aplicación para Gmail
3. **Actualizar** dependencias regularmente
4. **Habilitar** HTTPS en producción
5. **Configurar** límites de tasa (rate limiting)
6. **Monitorear** logs de seguridad

---

## 🐛 Solución de Problemas

### Errores Comunes

#### 1. "DisallowedHost"
**Problema**: Django rechaza la solicitud  
**Solución**:
```python
# settings.py
ALLOWED_HOSTS = ['tu-dominio.com', 'localhost', '127.0.0.1']
```

#### 2. "Static files not found"
**Problema**: CSS/JS no se cargan  
**Solución**:
```bash
python manage.py collectstatic --noinput
```

#### 3. "Database connection failed"
**Problema**: No puede conectar a la BD  
**Solución**:
- Verificar `DATABASE_URL` en variables de entorno
- Verificar credenciales de PostgreSQL

#### 4. "Module not found"
**Problema**: Falta una dependencia  
**Solución**:
```bash
pip install -r requirements.txt
```

#### 5. "CSRF verification failed"
**Problema**: Token CSRF inválido  
**Solución**:
- Verificar que el formulario incluya `{% csrf_token %}`
- Limpiar cookies del navegador

#### 6. "Email not sending"
**Problema**: Emails no se envían  
**Solución**:
- Verificar configuración SMTP
- Usar App Password de Gmail
- Verificar `EMAIL_BACKEND` en settings

### Logs y Debugging

#### Ver logs en desarrollo:
```bash
python manage.py runserver --verbosity 2
```

#### Ver logs en producción:
```bash
# PythonAnywhere
tail -f /var/log/tu-usuario.pythonanywhere.com.error.log

# Render
Ver en Dashboard → Logs

# Railway
Ver en Dashboard → Deployments → Logs
```

---

## 📈 Mejoras Futuras

### Fase 2 - Funcionalidades Adicionales

#### 1. Sistema de Pagos
- [ ] Integración con Stripe/PayPal
- [ ] Pagos con tarjeta
- [ ] Historial de transacciones
- [ ] Facturas electrónicas

#### 2. Sistema de Delivery
- [ ] Integración con Google Maps
- [ ] Cálculo de distancia y costo
- [ ] Seguimiento en tiempo real
- [ ] Asignación de repartidores

#### 3. Programa de Fidelidad
- [ ] Sistema de puntos
- [ ] Cupones y descuentos
- [ ] Niveles de membresía
- [ ] Recompensas

#### 4. Análisis Avanzado
- [ ] Dashboard de analytics
- [ ] Predicción de demanda
- [ ] Análisis de tendencias
- [ ] Reportes personalizados

#### 5. App Móvil
- [ ] Aplicación iOS
- [ ] Aplicación Android
- [ ] Notificaciones push
- [ ] Pedidos offline

#### 6. Integraciones
- [ ] WhatsApp Business API
- [ ] Redes sociales
- [ ] Sistemas de punto de venta
- [ ] Contabilidad

---

## 📖 Glosario

### Términos Técnicos

**MVT**: Modelo-Vista-Template, patrón arquitectónico de Django

**ORM**: Object-Relational Mapping, mapeo objeto-relacional

**CRUD**: Create, Read, Update, Delete - operaciones básicas

**CSRF**: Cross-Site Request Forgery, ataque de falsificación de petición

**WSGI**: Web Server Gateway Interface, interfaz entre servidor web y aplicación

**Middleware**: Software que actúa como puente entre aplicaciones

**Migration**: Archivo que describe cambios en la base de datos

**QuerySet**: Colección de objetos de la base de datos

**Template Tag**: Etiqueta especial en templates de Django

**Context**: Diccionario de variables pasadas a un template

### Términos del Negocio

**Pedido**: Orden realizada por un cliente

**Reserva**: Reservación de mesa para fecha/hora específica

**Plato**: Item del menú disponible para ordenar

**Inventario**: Stock de productos disponibles

**Dashboard**: Panel de control con métricas

**Reporte**: Documento con información del sistema

---

---

## 📊 Arquitectura del Sistema

### Patrón MVT (Modelo-Vista-Template)

El proyecto sigue el patrón arquitectónico MVT de Django:

#### **Modelos (Models)**
Definen la estructura de datos y la lógica de negocio:

- **Usuario**: Gestión de usuarios con roles (Cliente, Mesero, Administrador)
- **Plato**: Información de platos del menú
- **Pedido**: Órdenes de clientes
- **PedidoItem**: Items individuales de cada pedido
- **Reserva**: Reservas de mesas
- **Producto**: Inventario de productos

#### **Vistas (Views)**
Procesan las solicitudes y retornan respuestas:

- **Vistas basadas en funciones**: Para operaciones simples
- **Vistas basadas en clases**: Para operaciones CRUD complejas
- **Mixins de autenticación**: Control de acceso por rol

#### **Templates**
Presentan la información al usuario:

- **Templates base**: Estructura común (navbar, sidebar, footer)
- **Templates de componentes**: Elementos reutilizables
- **Templates específicos**: Para cada funcionalidad

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Navegador)                   │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   DJANGO FRAMEWORK                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │              URLs (urls.py)                       │  │
│  │         Enrutamiento de solicitudes               │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                      │
│  ┌────────────────▼─────────────────────────────────┐  │
│  │            VISTAS (views.py)                      │  │
│  │  • Lógica de negocio                             │  │
│  │  • Validaciones                                   │  │
│  │  • Servicios externos                            │  │
│  └────────┬──────────────────────┬──────────────────┘  │
│           │                      │                       │
│  ┌────────▼────────┐    ┌───────▼──────────┐          │
│  │  MODELOS        │    │   TEMPLATES      │          │
│  │  (models.py)    │    │   (HTML/CSS/JS)  │          │
│  │  • ORM Django   │    │   • TailwindCSS  │          │
│  │  • Validaciones │    │   • Alpine.js    │          │
│  └────────┬────────┘    └──────────────────┘          │
│           │                                              │
└───────────┼──────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────┐
│                  BASE DE DATOS (SQLite)                   │
│  • Usuarios  • Pedidos  • Reservas  • Inventario        │
└───────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modelado de Datos

### Diagrama Entidad-Relación

```
┌─────────────────┐
│    Usuario      │
│─────────────────│
│ id (PK)         │
│ username        │
│ email           │
│ password        │
│ rol             │
│ first_name      │
│ last_name       │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐         ┌─────────────────┐
│     Pedido      │    N    │   PedidoItem    │
│─────────────────│◄────────┤─────────────────│
│ id (PK)         │         │ id (PK)         │
│ cliente (FK)    │         │ pedido (FK)     │
│ fecha_pedido    │         │ producto (FK)   │
│ estado          │         │ nombre          │
│ total           │         │ cantidad        │
│ notas           │         │ precio_unitario │
└─────────────────┘         │ subtotal        │
                            └─────────────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│    Reserva      │
│─────────────────│
│ id (PK)         │
│ usuario (FK)    │
│ fecha_reserva   │
│ cantidad_personas│
│ estado          │
│ observaciones   │
└─────────────────┘

┌─────────────────┐
│    Producto     │
│─────────────────│
│ id (PK)         │
│ nombre          │
│ stock_actual    │
│ alerta_stock    │
│ precio          │
└─────────────────┘

┌─────────────────┐
│      Plato      │
│─────────────────│
│ id (PK)         │
│ nombre          │
│ descripcion     │
│ precio          │
│ categoria       │
│ imagen          │
│ disponible      │
└─────────────────┘
```

### Relaciones entre Modelos

1. **Usuario → Pedido**: Un usuario puede tener muchos pedidos (1:N)
2. **Usuario → Reserva**: Un usuario puede tener muchas reservas (1:N)
3. **Pedido → PedidoItem**: Un pedido tiene muchos items (1:N)
4. **Producto → PedidoItem**: Un producto puede estar en muchos items (1:N)

---

## 🔐 Sistema de Autenticación y Autorización

### Roles y Permisos

| Funcionalidad | Cliente | Mesero | Administrador |
|--------------|---------|--------|---------------|
| Ver menú | ✅ | ✅ | ✅ |
| Realizar pedidos | ✅ | ✅ | ✅ |
| Crear reservas | ✅ | ✅ | ✅ |
| Ver dashboard | ❌ | ✅ | ✅ |
| Actualizar estado pedidos | ❌ | ✅ | ✅ |
| Ver reportes | ❌ | ✅ | ✅ |
| Gestionar inventario | ❌ | ❌ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |
| Exportar reportes | ❌ | ✅ | ✅ |

### Flujo de Autenticación

```
1. Usuario accede a /login/
2. Ingresa credenciales
3. Django valida con authenticate()
4. Si es válido → login() y crea sesión
5. Redirección según rol:
   - Cliente → /menu/
   - Mesero/Admin → /dashboard/
```

---

## 📧 Sistema de Notificaciones por Email

### Tipos de Emails Automáticos

#### 1. Confirmación de Pedido
**Cuándo se envía**: Al crear un nuevo pedido  
**Contenido**:
- Número de pedido
- Lista de items
- Total a pagar
- Estado actual

#### 2. Cambio de Estado de Pedido
**Cuándo se envía**: Al actualizar el estado  
**Estados**:
- ⏳ Pendiente
- 👨‍🍳 En Preparación
- ✅ Listo
- 🎉 Entregado
- ❌ Cancelado

#### 3. Confirmación de Reserva
**Cuándo se envía**: Al crear una reserva  
**Contenido**:
- Número de reserva
- Fecha y hora
- Cantidad de personas
- Observaciones

#### 4. Cambio de Estado de Reserva
**Cuándo se envía**: Al actualizar o cancelar  
**Estados**:
- ⏳ Pendiente
- ✅ Confirmada
- ❌ Cancelada

### Configuración de Email

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_app_password'
DEFAULT_FROM_EMAIL = 'tu_email@gmail.com'
```

---

## 📊 Sistema de Reportes

### Tipos de Reportes Disponibles

#### 1. Reporte de Pedidos
**Filtros**:
- Fecha desde/hasta
- Estado del pedido
- Cliente específico

**Información incluida**:
- ID del pedido
- Cliente
- Fecha
- Estado
- Total
- Resumen de totales

#### 2. Reporte de Ventas
**Filtros**:
- Fecha desde/hasta
- Categoría de plato

**Métricas**:
- Total de ingresos
- Cantidad de pedidos
- Ticket promedio
- Top 10 platos más vendidos

#### 3. Reporte de Inventario
**Filtros**:
- Solo productos con stock bajo

**Información incluida**:
- Nombre del producto
- Stock actual
- Alerta de stock
- Precio unitario
- Valor total
- Alertas visuales

#### 4. Reporte de Reservas
**Filtros**:
- Fecha desde/hasta
- Estado de reserva

**Información incluida**:
- ID de reserva
- Cliente
- Fecha y hora
- Cantidad de personas
- Estado

### Formatos de Exportación

#### PDF
- Diseño profesional con logo
- Encabezados y pies de página
- Tablas estructuradas
- Colores corporativos
- Numeración de páginas

#### Excel
- Formato tabular
- Encabezados destacados
- Formato condicional
- Múltiples hojas
- Autoajuste de columnas

---

## 🎨 Diseño de Interfaz

### Paleta de Colores

```css
/* Colores Principales */
--primary: #d97706;      /* Amber 600 */
--primary-dark: #b45309; /* Amber 700 */
--primary-light: #fbbf24;/* Amber 400 */

/* Colores de Estado */
--success: #10b981;      /* Green 500 */
--warning: #f59e0b;      /* Amber 500 */
--error: #ef4444;        /* Red 500 */
--info: #3b82f6;         /* Blue 500 */

/* Modo Oscuro */
--dark-bg: #1f2937;      /* Gray 800 */
--dark-surface: #374151; /* Gray 700 */
--dark-text: #f9fafb;    /* Gray 50 */
```

### Componentes UI

#### Botones
```html
<!-- Primario -->
<button class="bg-amber-600 hover:bg-amber-700 text-white px-6 py-3 rounded-lg">
  Acción Principal
</button>

<!-- Secundario -->
<button class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg">
  Acción Secundaria
</button>

<!-- Peligro -->
<button class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg">
  Eliminar
</button>
```

#### Cards
```html
<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl transition-shadow">
  <!-- Contenido -->
</div>
```

### Responsive Design

```css
/* Breakpoints */
sm: 640px   /* Móviles grandes */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Pantallas grandes */
```

---

## 🧪 Testing

### Pruebas Unitarias

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una app específica
python manage.py test apps.pedidos

# Ejecutar con cobertura
coverage run --source='.' manage.py test
coverage report
```

### Pruebas Manuales Recomendadas

#### Autenticación
- [ ] Registro de nuevo usuario
- [ ] Login con credenciales correctas
- [ ] Login con credenciales incorrectas
- [ ] Logout
- [ ] Recuperación de contraseña

#### Pedidos
- [ ] Agregar items al carrito
- [ ] Eliminar items del carrito
- [ ] Realizar pedido
- [ ] Validación de stock
- [ ] Actualizar estado de pedido
- [ ] Recibir email de confirmación

#### Reservas
- [ ] Crear reserva
- [ ] Validación de fecha futura
- [ ] Actualizar reserva
- [ ] Cancelar reserva
- [ ] Recibir email de confirmación

#### Reportes
- [ ] Generar reporte PDF
- [ ] Generar reporte Excel
- [ ] Aplicar filtros
- [ ] Verificar datos correctos

---

## 🧪 Testing

Para ejecutar las pruebas:

```bash
python manage.py test
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 👥 Autores

- **Marlon Chamorro** - [marlonchamoro21@gmail.com](mailto:marlonchamoro21@gmail.com)
- **Equipo de Desarrollo** - [GitHub](https://github.com/Yesit21/Proyecto-finalDjango)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Django Documentation
- TailwindCSS Team
- Chart.js Community
- Todos los contribuidores del proyecto

---

## 📞 Soporte

Si tienes alguna pregunta o problema:

- 📧 Email: marlonchamoro21@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/Yesit21/Proyecto-finalDjango/issues)
- 📖 Documentación: Ver archivos `.md` en el repositorio

---

## 🔄 Actualizaciones

### Versión 1.0.0 (Mayo 2026)
- ✅ Sistema de autenticación completo
- ✅ Gestión de pedidos y reservas
- ✅ Dashboard con gráficos
- ✅ Sistema de reportes PDF/Excel
- ✅ Notificaciones por email
- ✅ Interfaz responsive con modo oscuro

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**


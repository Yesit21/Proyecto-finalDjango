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

### Opción 1: PythonAnywhere (Con SQLite)

1. Crea una cuenta en [PythonAnywhere](https://www.pythonanywhere.com/)
2. Sube tu código
3. Configura el entorno virtual
4. Configura el archivo WSGI
5. Recarga la aplicación

### Opción 2: Render (Con PostgreSQL)

1. Crea una cuenta en [Render](https://render.com/)
2. Crea un nuevo Web Service
3. Conecta tu repositorio de GitHub
4. Configura las variables de entorno
5. Despliega

### Opción 3: Railway (Con PostgreSQL)

1. Crea una cuenta en [Railway](https://railway.app/)
2. Crea un nuevo proyecto
3. Conecta tu repositorio
4. Agrega PostgreSQL
5. Configura variables de entorno
6. Despliega

**Documentación detallada de despliegue:** Ver `DESPLIEGUE.md`

---

## 📚 Documentación Adicional

- [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md) - Estado actual del proyecto
- [REPORTES_IMPLEMENTADOS.md](REPORTES_IMPLEMENTADOS.md) - Documentación del sistema de reportes
- [EMAILS_IMPLEMENTADOS.md](EMAILS_IMPLEMENTADOS.md) - Documentación del sistema de emails
- [PROGRESO_PROYECTO.md](PROGRESO_PROYECTO.md) - Progreso detallado del desarrollo

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


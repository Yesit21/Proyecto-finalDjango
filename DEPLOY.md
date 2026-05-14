# 🚀 Guía de Despliegue en Railway

## Requisitos Previos
- Cuenta en [Railway.app](https://railway.app)
- Repositorio Git con el código del proyecto
- Cuenta de Gmail para envío de emails (opcional)

## 📋 Pasos para Desplegar

### 1. Preparar el Repositorio

Asegúrate de que todos los cambios estén commiteados:

```bash
git add .
git commit -m "Preparar proyecto para despliegue en Railway"
git push origin main
```

### 2. Crear Proyecto en Railway

1. Ve a [Railway.app](https://railway.app) e inicia sesión
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway para acceder a tu repositorio
5. Selecciona el repositorio del proyecto

### 3. Agregar Base de Datos PostgreSQL

1. En tu proyecto de Railway, click en "New"
2. Selecciona "Database" → "Add PostgreSQL"
3. Railway creará automáticamente la variable `DATABASE_URL`

### 4. Configurar Variables de Entorno

En Railway, ve a tu servicio → "Variables" y agrega:

#### Variables Requeridas:
```
SECRET_KEY=tu-clave-secreta-super-segura-aqui-minimo-50-caracteres
DEBUG=False
```

#### Variables de Email (Opcionales pero recomendadas):
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-de-gmail
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

**Nota:** Para obtener una contraseña de aplicación de Gmail:
1. Ve a tu cuenta de Google → Seguridad
2. Activa la verificación en 2 pasos
3. Ve a "Contraseñas de aplicaciones"
4. Genera una nueva contraseña para "Correo"

### 5. Desplegar

Railway desplegará automáticamente tu aplicación. El proceso incluye:
- Instalar dependencias desde `requirements.txt`
- Ejecutar `collectstatic` para archivos estáticos
- Ejecutar migraciones de base de datos
- Iniciar el servidor con Gunicorn

### 6. Crear Superusuario

Una vez desplegado, necesitas crear un superusuario:

1. En Railway, ve a tu servicio
2. Click en la pestaña "Deployments"
3. Click en el deployment activo
4. Click en "View Logs"
5. En la parte superior, click en el ícono de terminal
6. Ejecuta:
```bash
python manage.py createsuperuser
```

### 7. Acceder a tu Aplicación

Railway te proporcionará una URL como:
```
https://tu-proyecto.up.railway.app
```

## 🔧 Comandos Útiles en Railway

### Ver logs en tiempo real:
En la terminal de Railway o en la sección "Deployments" → "View Logs"

### Ejecutar comandos:
1. Ve a "Deployments" → Click en el deployment activo
2. Click en el ícono de terminal
3. Ejecuta comandos como:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 📝 Archivos de Configuración Creados

- **Procfile**: Define cómo Railway debe ejecutar la aplicación
- **railway.toml**: Configuración específica de Railway
- **runtime.txt**: Especifica la versión de Python
- **requirements.txt**: Dependencias del proyecto

## ⚠️ Solución de Problemas

### Error: "Application failed to respond"
- Verifica que `ALLOWED_HOSTS` incluya tu dominio de Railway
- Revisa los logs en Railway para ver errores específicos

### Error: "Static files not loading"
- Ejecuta: `python manage.py collectstatic --noinput`
- Verifica que `STATIC_ROOT` esté configurado correctamente

### Error de Base de Datos
- Asegúrate de que PostgreSQL esté agregado al proyecto
- Verifica que `DATABASE_URL` esté en las variables de entorno
- Ejecuta las migraciones: `python manage.py migrate`

### Emails no se envían
- Verifica las credenciales de Gmail
- Asegúrate de usar una "Contraseña de aplicación" no tu contraseña normal
- Verifica que la verificación en 2 pasos esté activada en Gmail

## 🔒 Seguridad en Producción

Asegúrate de:
- ✅ `DEBUG=False` en producción
- ✅ `SECRET_KEY` único y seguro (mínimo 50 caracteres)
- ✅ No commitear el archivo `.env` al repositorio
- ✅ Usar contraseñas de aplicación para Gmail
- ✅ Revisar los logs regularmente

## 📚 Recursos Adicionales

- [Documentación de Railway](https://docs.railway.app/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 🎉 ¡Listo!

Tu aplicación debería estar funcionando en Railway. Accede a:
- **Frontend**: https://tu-proyecto.up.railway.app
- **Admin**: https://tu-proyecto.up.railway.app/admin/

# Configurar Email para Recuperación de Contraseña

## 📧 Configuración con Gmail

### 1. Habilitar verificación en 2 pasos
1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Seguridad → Verificación en 2 pasos
3. Actívala

### 2. Crear contraseña de aplicación
1. Ve a: https://myaccount.google.com/apppasswords
2. Selecciona "Correo" y "Otro (nombre personalizado)"
3. Escribe "Django Restaurante"
4. Copia la contraseña de 16 caracteres

### 3. Configurar archivo .env
Edita el archivo `.env` en la raíz del proyecto:

```env
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

**IMPORTANTE:** 
- Usa la contraseña de aplicación (16 caracteres), NO tu contraseña normal
- NO subas el archivo `.env` a Git (ya está en .gitignore)

### 4. Reiniciar servidor
```bash
# Detener servidor (Ctrl+C)
python manage.py runserver
```

## 🔧 Otras opciones de email

### SendGrid (Recomendado para producción)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-de-sendgrid
DEFAULT_FROM_EMAIL=tu-email-verificado@dominio.com
```

### Outlook/Hotmail
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña
```

## ✅ Probar configuración

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Prueba',
    'Email de prueba desde Django',
    'tu-email@gmail.com',
    ['destinatario@email.com'],
    fail_silently=False,
)
```

Si no hay errores, la configuración está correcta.

## 🚨 Solución de problemas

### Error: SMTPAuthenticationError
- Verifica que uses contraseña de aplicación, no tu contraseña normal
- Verifica que la verificación en 2 pasos esté activa

### Error: SMTPServerDisconnected
- Verifica EMAIL_PORT=587 y EMAIL_USE_TLS=True
- Verifica tu conexión a internet

### Los emails no llegan
- Revisa la carpeta de spam
- Verifica que DEFAULT_FROM_EMAIL sea el mismo que EMAIL_HOST_USER

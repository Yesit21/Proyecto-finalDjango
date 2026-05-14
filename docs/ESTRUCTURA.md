# Estructura del Proyecto

## Desarrollador 1 - Backend Core
- `core/` - Toda la carpeta
- `config/settings/` - Configuraciones
- `apps/usuarios/` - Autenticación
- `restaurante_project/` - URLs principales
- `utils/` - Utilidades compartidas

## Desarrollador 2 - Frontend Global
- `templates/` - Todos los templates
- `static/` - CSS, JS, imágenes
- `apps/menu/` - Menú y platos
- `apps/reservas/` - Reservas

## Desarrollador 3 - Pedidos y Reportes
- `apps/pedidos/` - Sistema de pedidos
- `apps/inventario/` - Control de inventario
- `apps/dashboard/` - Dashboard y reportes
- `services/reports/` - Generación de reportes
- `services/exports/` - Exportaciones

## Archivos Delicados (Requieren coordinación)
- `restaurante_project/settings.py`
- `restaurante_project/urls.py`
- `templates/base/base.html`
- `static/src/css/input.css`

## Flujo Git
```
main (producción)
  └── develop (desarrollo)
       ├── feature/dev1-auth
       ├── feature/dev2-frontend
       └── feature/dev3-reports
```

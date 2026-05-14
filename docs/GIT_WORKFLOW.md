# Flujo de Trabajo Git

## Ramas

### main
- Código en producción
- Solo merge desde develop
- Protegida

### develop
- Código en desarrollo
- Base para features
- Merge de features completados

### feature/*
- feature/dev1-auth
- feature/dev2-frontend
- feature/dev3-reports

## Workflow

### 1. Crear feature branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/dev1-auth
```

### 2. Trabajar en feature
```bash
git add .
git commit -m "feat: implementar login"
git push origin feature/dev1-auth
```

### 3. Pull Request
- Crear PR desde feature hacia develop
- Revisión de código
- Resolver conflictos
- Merge

### 4. Actualizar develop local
```bash
git checkout develop
git pull origin develop
```

## Commits

### Formato
```
tipo: descripción corta

Descripción detallada (opcional)
```

### Tipos
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Documentación
- style: Formato, CSS
- refactor: Refactorización
- test: Tests
- chore: Mantenimiento

## Evitar Conflictos

### Desarrollador 1
- Trabajar solo en core/, config/, apps/usuarios/
- No tocar templates/ ni static/

### Desarrollador 2
- Trabajar solo en templates/, static/, apps/menu/, apps/reservas/
- No tocar core/ ni services/

### Desarrollador 3
- Trabajar solo en apps/pedidos/, apps/inventario/, apps/dashboard/, services/
- No tocar templates/base/ ni static/src/css/input.css

### Archivos Compartidos
- Coordinar cambios en settings.py
- Coordinar cambios en urls.py
- Coordinar cambios en base.html

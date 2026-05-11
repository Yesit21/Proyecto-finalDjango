# Instalación

## 1. Clonar repositorio
```bash
git clone <repo>
cd Proyecto-finalDjango
```

## 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 3. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

## 4. Instalar dependencias Node
```bash
npm install
```

## 5. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus valores
```

## 6. Compilar TailwindCSS
```bash
npm run build
```

## 7. Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 8. Crear superusuario
```bash
python manage.py createsuperuser
```

## 9. Ejecutar servidor
```bash
python manage.py runserver
```

## 10. En otra terminal, watch de Tailwind
```bash
npm run dev
```

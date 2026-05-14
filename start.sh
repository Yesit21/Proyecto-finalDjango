#!/bin/bash

# Run migrations
python manage.py migrate --noinput

# Start Gunicorn with PORT from environment or default to 8000
exec gunicorn restaurante_project.wsgi --bind "0.0.0.0:${PORT:-8000}" --log-file -

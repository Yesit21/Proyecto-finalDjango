#!/bin/bash

# Run migrations with --fake-initial to handle existing tables
python manage.py migrate --fake-initial --noinput

# Get PORT from environment, default to 8000
PORT=${PORT:-8000}

# Start Gunicorn
exec gunicorn restaurante_project.wsgi --bind "0.0.0.0:$PORT" --log-file -

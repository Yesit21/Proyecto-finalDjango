#!/bin/bash

# Delete SQLite database if it exists (fresh start)
if [ -f "/app/db.sqlite3" ]; then
    echo "Removing old SQLite database..."
    rm -f /app/db.sqlite3
fi

# Run migrations from scratch
python manage.py migrate --noinput

# Get PORT from environment, default to 8000
PORT=${PORT:-8000}

# Start Gunicorn
exec gunicorn restaurante_project.wsgi --bind "0.0.0.0:$PORT" --log-file -

#!/bin/bash
set -e

echo "=== Starting deployment ==="

# Delete SQLite database if it exists (fresh start)
if [ -f "/app/db.sqlite3" ]; then
    echo "Removing old SQLite database..."
    rm -f /app/db.sqlite3
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput
echo "Migrations completed successfully"

# Get PORT from environment, default to 8000
PORT=${PORT:-8000}

# Start Gunicorn
echo "Starting Gunicorn on port $PORT..."
exec gunicorn restaurante_project.wsgi \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

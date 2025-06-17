#!/bin/bash
set -e

# Set Django settings
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn
echo "Starting gunicorn..."
exec gunicorn app:app --bind 0.0.0.0:$PORT 
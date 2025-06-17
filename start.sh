#!/bin/bash
set -e

echo "Setting Django settings module..."
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django application..."
gunicorn app:app --bind 0.0.0.0:$PORT 
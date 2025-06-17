#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate

echo "Starting Django application..."
gunicorn upendo_bakery.wsgi:application --bind 0.0.0.0:$PORT 
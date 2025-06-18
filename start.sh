#!/bin/bash
set -e

# Set Django settings
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

echo "=================================================="
echo "Starting Upendo Bakery Application"
echo "=================================================="

# Check environment
if [ -n "$RENDER_EXTERNAL_HOSTNAME" ]; then
    echo "✓ Running on Render platform"
    echo "Hostname: $RENDER_EXTERNAL_HOSTNAME"
else
    echo "⚠ Running in local environment"
fi

# Check database configuration
if [ -n "$DATABASE_URL" ]; then
    echo "✓ DATABASE_URL is configured"
    echo "Database: PostgreSQL (persistent)"
else
    echo "✗ DATABASE_URL is not configured"
    echo "⚠ WARNING: Data will not persist on Render!"
    echo "Please set up a PostgreSQL database and configure DATABASE_URL"
fi

# Run database setup check
echo "Running database setup check..."
python manage.py setup_render_database

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create default admin user
python manage.py create_default_admin

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn
echo "Starting gunicorn server..."
echo "=================================================="
exec gunicorn upendo_bakery.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 
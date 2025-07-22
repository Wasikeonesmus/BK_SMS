#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Upendo Bakery deployment build..."

# Set Django settings module
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

# Print environment variables for debugging
echo "🔍 Environment variables:"
printenv | sort

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📂 Creating necessary directories..."
mkdir -p staticfiles
mkdir -p media

# Set proper permissions
chmod -R 755 staticfiles
chmod -R 755 media

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Create default data
echo "⚙️  Creating default data..."
python manage.py create_default_admin || echo "⚠️  Could not create default admin (might already exist)"
python manage.py create_default_categories || echo "⚠️  Could not create default categories (might already exist)"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# List files for debugging
echo "📋 Directory structure after build:"
ls -la
ls -la staticfiles/

echo "✅ Build completed successfully!"

# Start the application
echo "🚀 Starting application..."
exec gunicorn upendo_bakery.wsgi:application --bind 0.0.0.0:${PORT:-8000}
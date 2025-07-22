#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Upendo Bakery deployment build..."

# Set Django settings module
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create static files directory if it doesn't exist
mkdir -p staticfiles

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Create default data
echo "⚙️  Creating default data..."
python manage.py create_default_admin
python manage.py create_default_categories

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"
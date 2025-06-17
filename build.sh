#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Upendo Bakery deployment build..."

# Set Django settings module
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!" 
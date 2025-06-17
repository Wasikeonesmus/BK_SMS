#!/bin/bash

# Exit on any error
set -e

echo "Using fallback build (without Pillow)..."

# Install Python dependencies without Pillow
echo "Installing Python dependencies (without Pillow)..."
pip install --no-cache-dir -r requirements-no-pillow.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Fallback build completed successfully!"
echo "Note: Image processing features may be limited without Pillow." 
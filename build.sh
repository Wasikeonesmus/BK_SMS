#!/bin/bash

# Exit on any error
set -e

# Enable debug output
set -x

echo "🚀 Starting Upendo Bakery deployment build..."

# Set Django settings module
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

# Print environment variables for debugging
echo "🔍 Environment variables:"
printenv | sort

# Create necessary directories with proper permissions
echo "📂 Creating necessary directories..."
mkdir -p staticfiles
mkdir -p media
chmod -R 755 staticfiles
chmod -R 755 media

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Check if we're using PostgreSQL
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  WARNING: DATABASE_URL is not set. Falling back to SQLite (not recommended for production)."
    # Create database directory if it doesn't exist
    mkdir -p $(dirname /tmp/db.sqlite3)
    touch /tmp/db.sqlite3
    chmod 755 /tmp/db.sqlite3
    export DATABASE_URL="sqlite:////tmp/db.sqlite3"
fi

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser if it doesn't exist..."
cat <<EOF | python manage.py shell || true
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

# Create default data
echo "⚙️  Creating default data..."
python manage.py create_default_admin 2>/dev/null || echo "⚠️  Could not create default admin (might already exist)"
python manage.py create_default_categories 2>/dev/null || echo "⚠️  Could not create default categories (might already exist)"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Set proper permissions for static files
chmod -R 755 staticfiles

# List files for debugging
echo "📋 Directory structure after build:"
pwd
ls -la
ls -la staticfiles/ || true

# Create a simple health check file
echo "🩺 Creating health check endpoint..."
mkdir -p staticfiles/health
cat > staticfiles/health/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Health Check</title>
</head>
<body>
    <h1>Health Check</h1>
    <p>Status: OK</p>
    <p>Time: $(date)</p>
</body>
</html>
EOF

echo "✅ Build completed successfully!"

# Start the application
echo "🚀 Starting application..."
exec gunicorn upendo_bakery.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --log-level=info \
    --access-logfile - \
    --error-logfile - \
    --capture-output
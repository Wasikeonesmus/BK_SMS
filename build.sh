#!/bin/bash
set -e  # Exit on error

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Set environment variables for the build process
export DJANGO_SETTINGS_MODULE=upendo_bakery.settings_prod

# Debug information
echo "=== Build Script Debug Info ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Verify Django is installed
echo "🔍 Checking Django installation..."
python -c "import django; print(f'Django version: {django.__version__}')"

# Set default port if not specified
export PORT=${PORT:-10000}

echo "🚀 Starting Upendo Bakery deployment build..."

# Print environment variables for debugging
echo "🔍 Environment variables:"
printenv | sort

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Debug database connection
echo "🔍 Checking database configuration..."
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  WARNING: DATABASE_URL is not set in environment variables."
    
    # Check for Render's internal database URL
    if [ -n "$RENDER_DATABASE_URL" ]; then
        echo "ℹ️  Found RENDER_DATABASE_URL, using it as DATABASE_URL"
        export DATABASE_URL="$RENDER_DATABASE_URL"
    # Check for Render's PostgreSQL database
    elif [ -n "$RENDER" ] && [ -n "$RENDER_DATABASE_INSTANCE_NAME" ]; then
        echo "ℹ️  Setting up Render PostgreSQL database connection"
        export DATABASE_URL="postgresql://$RENDER_DATABASE_USERNAME:$RENDER_DATABASE_PASSWORD@$RENDER_DATABASE_HOST:$RENDER_DATABASE_PORT/$RENDER_DATABASE_NAME"
    else
        echo "⚠️  No database configuration found. Falling back to SQLite (not recommended for production)."
        # Create a directory for SQLite database
        SQLITE_DIR=$(dirname "${SQLITE_PATH:-/tmp/db.sqlite3}")
        mkdir -p "$SQLITE_DIR"
        touch "${SQLITE_PATH:-/tmp/db.sqlite3}"
        chmod 755 "${SQLITE_PATH:-/tmp/db.sqlite3}"
        export DATABASE_URL="sqlite:///${SQLITE_PATH:-/tmp/db.sqlite3}"
    fi
fi

echo "🔗 Using DATABASE_URL: ${DATABASE_URL}"

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser if it doesn't exist..."
cat <<EOF | python manage.py shell
import os
from django.contrib.auth import get_user_model
User = get_user_model()

# Default credentials
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
EOF

# Create default data
echo "⚙️  Creating default data..."
python manage.py create_default_admin
python manage.py create_default_categories

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear
chmod -R 755 staticfiles

# Print directory structure for debugging
echo "📋 Directory structure after build:"
pwd
ls -la
ls -la staticfiles/

# Create a simple health check endpoint
echo "🩺 Creating health check endpoint..."
mkdir -p staticfiles/health
cat > staticfiles/health/index.html << 'EOL'
<!DOCTYPE html>
<html>
<head>
    <title>Health Check</title>
</head>
<body>
    <h1>Status: OK</h1>
    <p>Last updated: $(date)</p>
    <h3>Environment:</h3>
    <pre>$(env | sort)</pre>
</body>
</html>
EOL

echo "✅ Build completed successfully!"

echo "🚀 Starting application..."

# Start Gunicorn
exec gunicorn upendo_bakery.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 3 \
    --timeout 120 \
    --log-level=info \
    --access-logfile - \
    --error-logfile - \
    --capture-output

# If Gunicorn fails, start Django development server as fallback
echo "⚠️  Gunicorn failed, falling back to Django development server..."
python manage.py runserver 0.0.0.0:10000
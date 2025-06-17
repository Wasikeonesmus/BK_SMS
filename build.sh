#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Upendo Bakery deployment build..."
echo "=============================================="

# Ensure we're using pip, not poetry
export PIP_NO_CACHE_DIR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Update package list
echo "📦 Updating package list..."
apt-get update

# Install system dependencies for Pillow
echo "🔧 Installing system dependencies for Pillow..."
apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    libzbar0 \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    build-essential

# Set environment variables for Pillow
export CFLAGS="-I/usr/include"
export LDFLAGS="-L/usr/lib"
export PKG_CONFIG_PATH="/usr/lib/pkgconfig"

# Upgrade pip first
echo "🐍 Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Alternative: If Pillow fails, try installing without image processing
if [ $? -ne 0 ]; then
    echo "⚠️  Pillow installation failed, trying alternative approach..."
    pip install --no-cache-dir Django==5.2.1 django-phonenumber-field==7.3.0 phonenumbers==8.13.30 python-decouple==3.8 requests==2.31.0 django-crispy-forms==2.1 crispy-bootstrap5==2023.10 django-environ==0.11.2 psycopg2-binary==2.9.9 gunicorn==21.2.0 whitenoise==6.6.0 django-storages==1.14.2 python-dotenv==1.0.0 django-cors-headers==4.3.1 django-redis==5.4.0 sentry-sdk[django]==1.39.1 pytest==8.0.0 pytest-django==4.8.0 coverage==7.4.1 dj-database-url==2.1.0
    
    # Try installing Pillow separately with minimal features
    pip install --no-cache-dir --global-option=build_ext --global-option="--disable-jpeg" --global-option="--disable-zlib" --global-option="--disable-libjpeg" --global-option="--disable-libz" Pillow==9.5.0
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

echo "=============================================="
echo "✅ Build completed successfully!"
echo "🎉 Upendo Bakery is ready for deployment!" 
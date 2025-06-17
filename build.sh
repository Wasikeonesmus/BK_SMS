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

# Try installing simple requirements first (without Pillow)
echo "🐍 Installing Python dependencies (without Pillow)..."
pip install --no-cache-dir -r requirements-simple.txt

# Now try to install Pillow separately
echo "🐍 Installing Pillow..."
pip install --no-cache-dir Pillow==9.5.0

# If Pillow fails, try with minimal features
if [ $? -ne 0 ]; then
    echo "⚠️  Pillow installation failed, trying minimal build..."
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
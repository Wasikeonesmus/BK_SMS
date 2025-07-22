#!/bin/bash
set -e  # Exit on error

# Print environment info for debugging
echo "🔍 Render build script starting..."
echo "📂 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"
echo "📦 Pip version: $(pip --version)"

# Install system dependencies if needed
# echo "🔄 Installing system dependencies..."
# apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     python3-dev \
#     libpq-dev

# Upgrade pip and install Python dependencies
echo "📦 Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install any development dependencies if needed
# pip install -r requirements-dev.txt

# Make build.sh executable if it exists
if [ -f "build.sh" ]; then
    echo "✅ Found build.sh, making it executable..."
    chmod +x build.sh
    
    # Execute the build script
    echo "🚀 Executing build.sh..."
    exec ./build.sh
else
    echo "❌ Error: build.sh not found!"
    echo "📂 Current directory contents:"
    ls -la
    exit 1
fi

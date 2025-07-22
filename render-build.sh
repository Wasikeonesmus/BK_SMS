#!/bin/bash
set -e  # Exit on error

echo "🔍 Render build script starting..."
echo "📂 Current directory: $(pwd)"
echo "📋 Directory contents:"
ls -la

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

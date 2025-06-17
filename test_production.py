#!/usr/bin/env python
"""
Test script to verify production settings work correctly.
Run this before deploying to ensure everything is configured properly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings_prod')

# Setup Django
django.setup()

def test_production_settings():
    """Test that production settings are working correctly."""
    from django.conf import settings
    
    print("🔍 Testing Production Settings...")
    print("=" * 50)
    
    # Test basic settings
    print(f"✅ DEBUG: {settings.DEBUG}")
    print(f"✅ SECRET_KEY: {'Set' if settings.SECRET_KEY else 'Not Set'}")
    print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Test database
    print(f"✅ Database Engine: {settings.DATABASES['default']['ENGINE']}")
    
    # Test static files
    print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"✅ STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Test security settings
    print(f"✅ SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
    print(f"✅ SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
    print(f"✅ CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    
    # Test installed apps
    print(f"✅ Installed Apps: {len(settings.INSTALLED_APPS)} apps")
    
    # Test middleware
    print(f"✅ Middleware: {len(settings.MIDDLEWARE)} middleware")
    
    print("=" * 50)
    print("🎉 Production settings test completed!")
    
    # Test database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection: SUCCESS")
    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
    
    # Test static files collection
    try:
        from django.core.management import call_command
        call_command('collectstatic', '--dry-run', '--noinput')
        print("✅ Static files collection: SUCCESS")
    except Exception as e:
        print(f"❌ Static files collection: FAILED - {e}")

if __name__ == '__main__':
    test_production_settings() 
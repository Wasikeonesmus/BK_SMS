#!/usr/bin/env python3
"""
Quick fix script for Render database persistence issue.
This script helps diagnose and fix the DATABASE_URL configuration problem.
"""

import os
import sys
import subprocess
import requests
from urllib.parse import urlparse

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_success(message):
    print(f"✓ {message}")

def print_error(message):
    print(f"✗ {message}")

def print_warning(message):
    print(f"⚠ {message}")

def check_environment():
    """Check if we're running on Render"""
    print_header("ENVIRONMENT CHECK")
    
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_hostname:
        print_success(f"Running on Render: {render_hostname}")
        return True
    else:
        print_warning("Not running on Render (local environment)")
        return False

def check_database_url():
    """Check DATABASE_URL configuration"""
    print_header("DATABASE URL CHECK")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print_success("DATABASE_URL is configured")
        
        # Parse the URL to show connection details (without credentials)
        try:
            parsed = urlparse(database_url)
            print(f"Database type: {parsed.scheme}")
            print(f"Host: {parsed.hostname}")
            print(f"Port: {parsed.port}")
            print(f"Database: {parsed.path[1:]}")  # Remove leading slash
            return True
        except Exception as e:
            print_error(f"Invalid DATABASE_URL format: {e}")
            return False
    else:
        print_error("DATABASE_URL is not configured")
        print_warning("This will cause data loss on Render!")
        return False

def check_django_settings():
    """Check Django database configuration"""
    print_header("DJANGO DATABASE CHECK")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings_prod')
        
        import django
        django.setup()
        
        from django.conf import settings
        db_engine = settings.DATABASES['default']['ENGINE']
        
        if 'postgresql' in db_engine:
            print_success("Django configured for PostgreSQL")
            return True
        elif 'sqlite' in db_engine:
            print_warning("Django configured for SQLite (data will not persist)")
            return False
        else:
            print_warning(f"Unknown database engine: {db_engine}")
            return False
            
    except Exception as e:
        print_error(f"Error checking Django settings: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print_header("DATABASE CONNECTION TEST")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings_prod')
        
        import django
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print_success("Database connection successful")
            
            # Get database version
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"Database version: {version}")
            
            return True
            
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        return False

def provide_fix_instructions():
    """Provide step-by-step fix instructions"""
    print_header("FIX INSTRUCTIONS")
    
    print("Your application is running on Render without a PostgreSQL database.")
    print("Follow these steps to fix the data persistence issue:\n")
    
    print("STEP 1: Create PostgreSQL Database")
    print("1. Go to https://dashboard.render.com")
    print("2. Click 'New' → 'PostgreSQL'")
    print("3. Configure:")
    print("   - Name: upendo-bakery-db")
    print("   - Plan: Free")
    print("   - Region: Same as your web service")
    print("4. Click 'Create Database'")
    print()
    
    print("STEP 2: Link Database to Web Service")
    print("1. Go to your web service settings")
    print("2. Click 'Environment' tab")
    print("3. Add environment variable:")
    print("   - Key: DATABASE_URL")
    print("   - Value: Copy from database service settings")
    print()
    
    print("STEP 3: Redeploy Application")
    print("1. Click 'Manual Deploy' → 'Deploy latest commit'")
    print("2. Wait for deployment to complete")
    print("3. Check the health endpoint: https://your-app.onrender.com/health/")
    print()
    
    print("ALTERNATIVE: Use render.yaml (Recommended)")
    print("1. Ensure your render.yaml includes the database configuration")
    print("2. Redeploy from Git repository")
    print("3. Render will automatically create and link the database")
    print()
    
    print("MONITORING:")
    print("- Health check: https://your-app.onrender.com/health/")
    print("- Database monitoring: python manage.py monitor_database")
    print("- Setup check: python manage.py setup_render_database")

def check_health_endpoint():
    """Check if health endpoint is accessible"""
    print_header("HEALTH ENDPOINT CHECK")
    
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if not render_hostname:
        print_warning("Cannot check health endpoint (not on Render)")
        return
    
    health_url = f"https://{render_hostname}/health/"
    
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print_success("Health endpoint accessible")
            data = response.json()
            print(f"Status: {data.get('status', 'unknown')}")
            print(f"Database: {data.get('database', 'unknown')}")
            print(f"Data persistence: {data.get('data_persistence', 'unknown')}")
        else:
            print_error(f"Health endpoint returned status {response.status_code}")
    except Exception as e:
        print_error(f"Health endpoint not accessible: {e}")

def main():
    """Main function"""
    print_header("RENDER DATABASE PERSISTENCE FIX")
    print("This script will help you diagnose and fix the data persistence issue on Render.\n")
    
    # Run checks
    is_render = check_environment()
    has_database_url = check_database_url()
    django_configured = check_django_settings()
    connection_works = test_database_connection()
    
    if is_render:
        check_health_endpoint()
    
    # Summary
    print_header("SUMMARY")
    
    if is_render and has_database_url and django_configured and connection_works:
        print_success("Everything is configured correctly!")
        print("Your application should have data persistence on Render.")
    else:
        print_error("Issues detected with database configuration")
        if is_render and not has_database_url:
            print_warning("CRITICAL: No DATABASE_URL on Render - data will be lost!")
            provide_fix_instructions()
        elif not connection_works:
            print_warning("Database connection failed - check your configuration")
        else:
            print_warning("Some configuration issues detected")
    
    print("\nFor more information, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 
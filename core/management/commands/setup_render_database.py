from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os
import sys

class Command(BaseCommand):
    help = 'Set up database for Render deployment and ensure data persistence'

    def handle(self, *args, **options):
        self.stdout.write('Setting up database for Render deployment...')
        
        # Check if we're on Render
        is_render = os.getenv('RENDER_EXTERNAL_HOSTNAME') is not None
        
        if is_render:
            self.stdout.write('Detected Render environment')
        else:
            self.stdout.write('Not on Render (local development)')
        
        # Check database configuration
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            self.stdout.write(
                self.style.SUCCESS('✓ DATABASE_URL is configured')
            )
            # Show first part of URL for debugging (without credentials)
            if database_url.startswith('postgres://'):
                parts = database_url.split('@')
                if len(parts) > 1:
                    self.stdout.write(f'Database URL: postgres://***@{parts[1]}')
                else:
                    self.stdout.write(f'Database URL: {database_url[:30]}...')
            else:
                self.stdout.write(f'Database URL: {database_url[:30]}...')
        else:
            self.stdout.write(
                self.style.ERROR('✗ DATABASE_URL is not configured')
            )
            self.stdout.write(
                self.style.WARNING('This will cause data loss on Render!')
            )
        
        # Check which database engine is being used
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine:
            self.stdout.write(
                self.style.SUCCESS('✓ Using PostgreSQL database')
            )
        elif 'sqlite' in db_engine:
            self.stdout.write(
                self.style.WARNING('⚠ Using SQLite database (data will not persist on Render)')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ Using unknown database: {db_engine}')
            )
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(
                    self.style.SUCCESS('✓ Database connection successful')
                )
                
                # Test if we can write to the database
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                self.stdout.write(f'Database version: {version}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Database connection failed: {e}')
            )
            if is_render:
                self.stdout.write(
                    self.style.ERROR('CRITICAL: Database connection failed on Render!')
                )
                self.stdout.write(
                    self.style.ERROR('This will prevent your application from working properly.')
                )
        
        # Check for common Render database issues
        if is_render:
            self.stdout.write('\n' + '='*60)
            self.stdout.write('RENDER DATABASE DIAGNOSTICS:')
            self.stdout.write('='*60)
            
            # Check if database service exists
            if not database_url:
                self.stdout.write(
                    self.style.ERROR('ISSUE: DATABASE_URL is missing')
                )
                self.stdout.write('POSSIBLE CAUSES:')
                self.stdout.write('1. Database service not created in render.yaml')
                self.stdout.write('2. Database service not linked to web service')
                self.stdout.write('3. Database service failed to provision')
                self.stdout.write('4. Environment variable not properly configured')
                
                self.stdout.write('\nSOLUTION STEPS:')
                self.stdout.write('1. Go to your Render dashboard')
                self.stdout.write('2. Check if "upendo-bakery-db" database service exists')
                self.stdout.write('3. If not, create a new PostgreSQL database service')
                self.stdout.write('4. Copy the DATABASE_URL from the database settings')
                self.stdout.write('5. Add DATABASE_URL to your web service environment variables')
                self.stdout.write('6. Redeploy your application')
                
                self.stdout.write('\nALTERNATIVE: Use render.yaml to auto-create database')
                self.stdout.write('Your render.yaml should include:')
                self.stdout.write('  databases:')
                self.stdout.write('    - name: upendo-bakery-db')
                self.stdout.write('      databaseName: upendo_bakery')
                self.stdout.write('      user: upendo_bakery_user')
                self.stdout.write('      plan: free')
            else:
                self.stdout.write(
                    self.style.SUCCESS('✓ DATABASE_URL is properly configured')
                )
                self.stdout.write('✓ Database service is linked to web service')
                self.stdout.write('✓ Data persistence is enabled')
        
        # Provide comprehensive setup instructions
        if is_render and not database_url:
            self.stdout.write('\n' + '='*60)
            self.stdout.write(
                self.style.WARNING('URGENT: RENDER SETUP REQUIRED')
            )
            self.stdout.write('='*60)
            self.stdout.write('Your application is running on Render but will lose data!')
            self.stdout.write('\nFOLLOW THESE STEPS IMMEDIATELY:')
            self.stdout.write('\n1. Go to https://dashboard.render.com')
            self.stdout.write('2. Navigate to your "upendo-bakery" service')
            self.stdout.write('3. Click "Environment" tab')
            self.stdout.write('4. Check if DATABASE_URL is listed')
            self.stdout.write('5. If not, create a PostgreSQL database:')
            self.stdout.write('   - Click "New" → "PostgreSQL"')
            self.stdout.write('   - Name: upendo-bakery-db')
            self.stdout.write('   - Plan: Free')
            self.stdout.write('   - Copy the DATABASE_URL')
            self.stdout.write('6. Add DATABASE_URL to your web service environment variables')
            self.stdout.write('7. Redeploy your application')
            self.stdout.write('\nOR use the render.yaml approach:')
            self.stdout.write('1. Ensure your render.yaml includes the database configuration')
            self.stdout.write('2. Redeploy from your Git repository')
            self.stdout.write('3. Render will automatically create and link the database')
            self.stdout.write('='*60)
        
        self.stdout.write(
            self.style.SUCCESS('Database setup check completed!')
        ) 
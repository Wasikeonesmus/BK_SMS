from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os

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
            self.stdout.write(f'Database URL: {database_url[:20]}...')
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
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Database connection failed: {e}')
            )
        
        # Provide instructions for Render setup
        if is_render and not database_url:
            self.stdout.write('\n' + '='*50)
            self.stdout.write(
                self.style.WARNING('RENDER SETUP INSTRUCTIONS:')
            )
            self.stdout.write('1. Go to your Render dashboard')
            self.stdout.write('2. Create a new PostgreSQL database')
            self.stdout.write('3. Copy the DATABASE_URL from the database settings')
            self.stdout.write('4. Add DATABASE_URL to your web service environment variables')
            self.stdout.write('5. Redeploy your application')
            self.stdout.write('='*50)
        
        self.stdout.write(
            self.style.SUCCESS('Database setup check completed!')
        ) 
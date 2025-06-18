from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
import os
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Monitor database health and performance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run continuous monitoring',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Monitoring interval in seconds (default: 60)',
        )

    def handle(self, *args, **options):
        if options['continuous']:
            self.stdout.write('Starting continuous database monitoring...')
            self.stdout.write(f'Monitoring interval: {options["interval"]} seconds')
            self.stdout.write('Press Ctrl+C to stop\n')
            
            try:
                while True:
                    self.check_database_health()
                    time.sleep(options['interval'])
            except KeyboardInterrupt:
                self.stdout.write('\nMonitoring stopped.')
        else:
            self.check_database_health()

    def check_database_health(self):
        """Check database health and performance"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(f'\n[{timestamp}] Database Health Check:')
        self.stdout.write('=' * 50)
        
        # Check environment
        is_render = os.getenv('RENDER_EXTERNAL_HOSTNAME') is not None
        database_url = os.getenv('DATABASE_URL')
        
        self.stdout.write(f'Environment: {"Render" if is_render else "Local"}')
        self.stdout.write(f'Database URL configured: {"Yes" if database_url else "No"}')
        
        # Check database engine
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine:
            self.stdout.write(
                self.style.SUCCESS('✓ Using PostgreSQL database')
            )
        elif 'sqlite' in db_engine:
            self.stdout.write(
                self.style.WARNING('⚠ Using SQLite database')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ Using {db_engine}')
            )
        
        # Test connection
        try:
            start_time = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                connection_time = (time.time() - start_time) * 1000
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Database connection successful ({connection_time:.2f}ms)')
                )
                
                # Get database info
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                self.stdout.write(f'Database version: {version}')
                
                # Check table count
                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                table_count = cursor.fetchone()[0]
                self.stdout.write(f'Table count: {table_count}')
                
                # Check for core tables
                core_tables = ['core_user', 'core_product', 'core_order', 'core_customer']
                missing_tables = []
                
                for table in core_tables:
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = %s
                        )
                    """, [table])
                    exists = cursor.fetchone()[0]
                    if not exists:
                        missing_tables.append(table)
                
                if missing_tables:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Missing tables: {", ".join(missing_tables)}')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS('✓ All core tables present')
                    )
                
                # Check data counts
                try:
                    cursor.execute("SELECT COUNT(*) FROM core_user")
                    user_count = cursor.fetchone()[0]
                    self.stdout.write(f'User count: {user_count}')
                    
                    cursor.execute("SELECT COUNT(*) FROM core_product")
                    product_count = cursor.fetchone()[0]
                    self.stdout.write(f'Product count: {product_count}')
                    
                    cursor.execute("SELECT COUNT(*) FROM core_order")
                    order_count = cursor.fetchone()[0]
                    self.stdout.write(f'Order count: {order_count}')
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Could not get data counts: {e}')
                    )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Database connection failed: {e}')
            )
            
            if is_render and not database_url:
                self.stdout.write(
                    self.style.ERROR('CRITICAL: No DATABASE_URL on Render!')
                )
                self.stdout.write(
                    self.style.ERROR('Data will be lost on container restart!')
                )
        
        # Data persistence warning
        if is_render and not database_url:
            self.stdout.write('\n' + '!' * 60)
            self.stdout.write(
                self.style.ERROR('DATA PERSISTENCE WARNING')
            )
            self.stdout.write('!' * 60)
            self.stdout.write('Your application is running on Render without a PostgreSQL database.')
            self.stdout.write('All data will be lost when the container restarts.')
            self.stdout.write('\nTo fix this:')
            self.stdout.write('1. Create a PostgreSQL database on Render')
            self.stdout.write('2. Set the DATABASE_URL environment variable')
            self.stdout.write('3. Redeploy your application')
            self.stdout.write('!' * 60)
        
        self.stdout.write('=' * 50) 
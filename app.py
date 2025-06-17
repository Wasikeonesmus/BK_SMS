import os
import sys
import django
import subprocess

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings_prod')

# Debug: Print environment variables
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")

# Initialize Django
django.setup()

# Run migrations and collect static files on startup
def run_setup_commands():
    try:
        print("Running database migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("Migrations completed successfully")
        else:
            print(f"Migration failed: {result.stderr}")
            print("Continuing without migrations...")
    except subprocess.TimeoutExpired:
        print("Migration timed out, continuing...")
    except Exception as e:
        print(f"Error running migrations: {e}")
        print("Continuing without migrations...")
    
    try:
        print("Collecting static files...")
        result = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("Static files collected successfully")
        else:
            print(f"Static collection failed: {result.stderr}")
            print("Continuing without static collection...")
    except subprocess.TimeoutExpired:
        print("Static collection timed out, continuing...")
    except Exception as e:
        print(f"Error collecting static files: {e}")
        print("Continuing without static collection...")

# Run setup commands
run_setup_commands()

# Import the WSGI application
from upendo_bakery.wsgi import application

# Export the application for gunicorn
app = application 
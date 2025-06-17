import os
import sys
import django
import subprocess

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings_prod')

# Initialize Django
django.setup()

# Run migrations and collect static files on startup
def run_setup_commands():
    try:
        print("Running database migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True, capture_output=True, text=True)
        print("Migrations completed successfully")
        
        print("Collecting static files...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True, capture_output=True, text=True)
        print("Static files collected successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running setup commands: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error during setup: {e}")

# Run setup commands
run_setup_commands()

# Import the WSGI application
from upendo_bakery.wsgi import application

# Export the application for gunicorn
app = application 
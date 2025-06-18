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
        print("Ensuring data persistence...")
        result = subprocess.run([sys.executable, 'manage.py', 'ensure_data_persistence'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Data persistence ensured successfully")
        else:
            print(f"Data persistence failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Data persistence timed out")
    except Exception as e:
        print(f"Error ensuring data persistence: {e}")
    
    try:
        print("Creating default admin user...")
        result = subprocess.run([sys.executable, 'manage.py', 'create_default_admin'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Default admin user created successfully")
        else:
            print(f"Admin user creation failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Admin user creation timed out")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    
    try:
        print("Creating default categories...")
        result = subprocess.run([sys.executable, 'manage.py', 'create_default_categories'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Default categories created successfully")
        else:
            print(f"Category creation failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Category creation timed out")
    except Exception as e:
        print(f"Error creating categories: {e}")
    
    try:
        print("Checking database setup...")
        result = subprocess.run([sys.executable, 'manage.py', 'setup_render_database'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Database setup check completed")
            print(result.stdout)
        else:
            print(f"Database setup check failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Database setup check timed out")
    except Exception as e:
        print(f"Error checking database setup: {e}")
    
    try:
        print("Collecting static files...")
        result = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("Static files collected successfully")
        else:
            print(f"Static collection failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Static collection timed out")
    except Exception as e:
        print(f"Error collecting static files: {e}")

# Run setup commands
run_setup_commands()

# Import the WSGI application
from upendo_bakery.wsgi import application as app 
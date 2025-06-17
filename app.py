import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings_prod')

# Initialize Django
django.setup()

# Import the WSGI application
from upendo_bakery.wsgi import application

# Export the application for gunicorn
app = application 
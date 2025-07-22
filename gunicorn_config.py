import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Set the working directory to the project root
chdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Explicitly set the WSGI application
wsgi_app = 'upendo_bakery.wsgi:application'

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'

# Process naming
proc_name = 'upendo_bakery'

# SSL (only used if SSL is configured)
keyfile = os.getenv('SSL_KEYFILE')
certfile = os.getenv('SSL_CERTFILE') 
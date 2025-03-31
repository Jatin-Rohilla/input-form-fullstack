"""Gunicorn configuration for Render deployment."""

import os

# Get the PORT from environment variable
port = os.environ.get("PORT", 8000)

# Bind to the port on all interfaces
bind = f"0.0.0.0:{port}"

# Worker configurations
workers = 4
worker_class = "gevent"
threads = 2

# Timeout settings
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Set application module
wsgi_app = "core.wsgi:application"

# Reload on code changes (for development only)
reload = os.environ.get("DEBUG", "False") == "True" 
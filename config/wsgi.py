"""
NUJ India — WSGI Configuration

Exposes the WSGI callable as a module-level variable named 'application'.
For local development this defaults to development settings; override via
the DJANGO_SETTINGS_MODULE env variable in production.
"""
import os
from django.core.wsgi import get_wsgi_application

# Default to development. Production deployments must set the env var explicitly.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_wsgi_application()

"""
NUJ India — Development Settings
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

# Use Django debug toolbar in development (optional)
INTERNAL_IPS = ['127.0.0.1']

# Email — print to console in dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files — use simple storage in dev (no manifest needed)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Admin URL
ADMIN_URL = 'nuj-admin/'

# Membership & Contact emails (dev)
MEMBERSHIP_EMAIL = 'membership@nujindia.org'
CONTACT_EMAIL = 'contact@nujindia.org'

# Site URL for dev
SITE_URL = 'http://localhost:8000'

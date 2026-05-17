import os
from django.core.wsgi import get_wsgi_application

# Force the settings to production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Create the 'app' object that Render/Gunicorn is looking for
app = get_wsgi_application()

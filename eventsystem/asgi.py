"""ASGI config for eventsystem project."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventsystem.settings')
application = get_asgi_application()

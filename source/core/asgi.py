"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``core``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

core = get_asgi_application()
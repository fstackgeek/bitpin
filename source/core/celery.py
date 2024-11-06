import os

from celery import Celery
from django.conf import settings

env = (os.environ.get('ENV') or 'DEVELOPMENT').lower()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'source.core.settings.{env}')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

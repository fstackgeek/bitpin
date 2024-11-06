import json
import os

from .default import *

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = json.loads(os.environ.get('ALLOWED_HOSTS'))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.environ.get('LOG_LEVEL', 'WARNING')
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{os.environ.get('REDIS_HOST')}:{os.environ.get("REDIS_PORT")}/{os.environ.get("REDIS_DB")}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'psqlextra.backend',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

CELERY_BROKER_URL = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/{os.environ.get("REDIS_DB")}'
CELERY_RESULT_BACKEND = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/{os.environ.get("REDIS_DB")}'

CELERY_BEAT_INTERVAL = int(os.environ.get('CELERY_BEAT_INTERVAL', 1.0))

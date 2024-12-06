from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')
INSTALLED_APPS = [
    'app',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'rest_framework'
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = os.getenv('URLCONF')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WSGI_APPLICATION = 'web.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = os.getenv('STATIC_URL')
STATIC_ROOT = BASE_DIR / "staticfiles"

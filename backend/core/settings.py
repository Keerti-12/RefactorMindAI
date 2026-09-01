from pathlib import Path
from dotenv import load_dotenv
import os

#Paths
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR.parent / '.env')

#Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-fallback-key-change-in-prod')
DEBUG = os.getenv('DEBUG', 'True') == True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

#Apps
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'corsheaders',
    'api',
    'jobs',
]

#Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

#URLs & WSGI
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATIONS = 'core.wsgi.application'

#SQLite3 DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR/ 'dev_db.sqlite3'
    }
}

#Celery 
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

#Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERED_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

#CORS
CORS_ALLOWED_ORIGINS = [
    'https://localhost:3000'
]

#Defaults
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAUGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the .env file
load_dotenv()

# Database settings using the DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600, ssl_require=True)
}

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django Rest Framework
    'corsheaders',      # For handling cross-origin requests
    # Custom apps
    'accounts',         # User authentication app
    'trading',  
    'stock'  ,              # Stock trading core app
    'dashboard', 
    'controller' ,
    'userprofile'    ,  # User dashboard app
    'portifolio',
    'transactions',
    'stockPriceHistory'
]

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for development. Restrict in production.

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add corsheaders middleware first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files configuration
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Central static folder
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files directory
STATIC_URL = '/static/'  # URL prefix for static files

# URL Configuration
ROOT_URLCONF = 'stock_simulator.urls'

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Main templates directory
        'APP_DIRS': True,  # Enable app-level template directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'stock_simulator.wsgi.application'

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # Adjust to 'Africa/Kigali' based on your location
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

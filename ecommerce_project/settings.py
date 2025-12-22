"""
Django settings for ecommerce_project project.
"""

from pathlib import Path
import os
import environ

# Initialize environment variables
env = environ.Env(
    # Set default values
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'default-insecure-key-change-in-production'),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
env_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(env_file):
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-zux+a@eggwlxlsm_b@^8$=z%!+1)+)m@1ztf2cgt6=@5gw*-j%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ERPNext Integration
ERPNEXT_ENABLED = True
ERPNEXT_URL = "http://127.0.0.1:8000"  # matches your ERPNext instance
ERPNEXT_API_KEY = os.getenv("ERPNEXT_API_KEY", "f140b62718e9c23")
ERPNEXT_API_SECRET = os.getenv("ERPNEXT_API_SECRET", "9a9df3be4f08a40")

ALLOWED_HOSTS = ['*']  # For development, in production set to specific domain

# Server port configuration
PORT = int(os.getenv('PORT', '9000'))

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.app',  # Allow all Replit domains
    'https://*.replit.dev', 
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:5000',
    'http://localhost:9000',
    'http://0.0.0.0:5000',
    'http://0.0.0.0:9000',
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # In development mode, allow all origins

# Cookie settings for iframe compatibility in Replit
# In development (HTTP), use 'Lax' instead of 'None'
CSRF_COOKIE_SAMESITE = 'Lax' if DEBUG else 'None'
CSRF_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read CSRF cookie if needed
SESSION_COOKIE_SAMESITE = 'Lax' if DEBUG else 'None'
SESSION_COOKIE_SECURE = False if DEBUG else True

# Allow serving in iframe
X_FRAME_OPTIONS = 'ALLOWALL' if DEBUG else 'SAMEORIGIN'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required by django-allauth

    # Third-party apps
    'corsheaders',  # CORS handling
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Local apps
    'store.apps.StoreConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS handling
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Required by django-allauth
]

ROOT_URLCONF = 'ecommerce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use something like:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_PORT = env('EMAIL_PORT', int)
# EMAIL_USE_TLS = env('EMAIL_USE_TLS', bool)
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
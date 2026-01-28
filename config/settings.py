"""
settings.py CORREGIDO - Sin error de Csv
"""

from pathlib import Path
import os
import sys

# Importar decouple
try:
    from decouple import config, Csv
except ImportError:
    def config(key, default=None, cast=None):
        value = os.environ.get(key, default)
        if cast and value:
            return cast(value)
        return value
    
    class Csv:
        def __call__(self, value):
            return [s.strip() for s in value.split(',')]
    Csv = Csv()

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

# ====================================
# SECURITY
# ====================================

SECRET_KEY = config('SECRET_KEY', default='django-insecure-' + os.urandom(24).hex())
DEBUG = config('DEBUG', default=True, cast=bool)

# ====================================
# ALLOWED_HOSTS - CORREGIDO
# ====================================

# FORMA CORRECTA: Convertir a lista primero
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv))

# Agregar hostname de Render
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default='')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ====================================
# INSTALLED APPS
# ====================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party - ORDEN IMPORTANTE
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',
    'phonenumber_field',
    
    # Local
    'curriculum',
]

# ====================================
# MIDDLEWARE
# ====================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ====================================
# TEMPLATES
# ====================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ====================================
# DATABASE
# ====================================

DATABASE_URL = config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')

if dj_database_url and 'postgres' in DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ====================================
# PASSWORD VALIDATION
# ====================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ====================================
# INTERNATIONALIZATION
# ====================================

LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# ====================================
# STATIC FILES
# ====================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ====================================
# CLOUDINARY
# ====================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

# Verificar si está configurado
CLOUDINARY_CONFIGURED = all([
    CLOUDINARY_STORAGE['CLOUD_NAME'],
    CLOUDINARY_STORAGE['API_KEY'],
    CLOUDINARY_STORAGE['API_SECRET']
])

# ====================================
# MEDIA FILES
# ====================================

if not DEBUG and CLOUDINARY_CONFIGURED:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

# ====================================
# AUTHENTICATION
# ====================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# ====================================
# MESSAGES
# ====================================

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ====================================
# CRISPY FORMS
# ====================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ====================================
# PHONE NUMBER
# ====================================

PHONENUMBER_DEFAULT_REGION = 'EC'
PHONENUMBER_DB_FORMAT = 'INTERNATIONAL'

# ====================================
# DEFAULT PRIMARY KEY
# ====================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================================
# SECURITY (PRODUCTION)
# ====================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ====================================
# LOGGING
# ====================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
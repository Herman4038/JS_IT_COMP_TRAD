from pathlib import Path
import os
from decouple import config

# ─── BASE ────────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')
DEBUG      = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', 
                       default='localhost 127.0.0.1 [::1]').split()

# ─── APPS & MIDDLEWARE ─────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.trading',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',           # ← WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',  # For session management
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # For user authentication
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── LOGIN & REDIRECT SETTINGS ───────────────────────────────────────────────────────

# URL for login page
LOGIN_URL = '/accounts/login/'  # Redirect to login if user is not authenticated
LOGIN_REDIRECT_URL = '/dashboard/'  # Redirect to dashboard after login

# ─── TEMPLATES ────────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],  # Path to your templates folder
        'APP_DIRS': True,
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

ROOT_URLCONF = 'js_it_comp_trad.urls'

WSGI_APPLICATION = 'js_it_comp_trad.wsgi.application'

# ─── DATABASE ───────────────────────────────────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='js_it_comp_trad'),
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='postgres'),
        'HOST': config('POSTGRES_HOST', default='db'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}

# ─── PASSWORD VALIDATION ────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# ─── SESSION SETTINGS ─────────────────────────────────────────────────────────────

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Database-backed sessions
SESSION_COOKIE_AGE = 60 * 60 * 24  # 1 day, adjust as needed

# ─── INTERNATIONALIZATION ───────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# ─── STATIC FILES ───────────────────────────────────────────────────────────────

STATIC_URL = '/static/'

# Where you keep your "raw" static assets in your repo:
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Where `collectstatic` will collect them for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use WhiteNoise’s compressed, manifest-based storage for cache busting:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─── MEDIA FILES ────────────────────────────────────────────────────────────────

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── DEFAULT PK FIELD TYPE ─────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

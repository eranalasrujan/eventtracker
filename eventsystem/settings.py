# eventsystem/settings.py

import os
from pathlib import Path

# ─── BASE_DIR ──────────────────────────────────────────────────────────────
# Points at the directory that contains manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SECURITY ──────────────────────────────────────────────────────────────
SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

# ─── INSTALLED APPS ────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',            # must come before your custom 'accounts'
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',                       # your custom user + registration
    'events',                         # your event & dashboard logic
]

# ─── MIDDLEWARE ────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── URLS & TEMPLATES ─────────────────────────────────────────────────────
ROOT_URLCONF = 'eventsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # global "/templates" for base.html, registration/, etc.
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # needed by auth views
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eventsystem.wsgi.application'

# ─── DATABASE ──────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── AUTHENTICATION ────────────────────────────────────────────────────────
# point to your custom user class
AUTH_USER_MODEL = 'accounts.CustomUser'

# after login, send everyone to /dashboard/ which will forward by role
LOGIN_REDIRECT_URL = '/dashboard/'
# after logout, back to the public event list
LOGOUT_REDIRECT_URL = '/'

# ─── PASS VALIDATION ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# ─── INTERNATIONALIZATION ──────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ─── STATIC FILES ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'
# for your own css/js under project/static/
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

# ─── DEFAULT PK TYPE ───────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# After a successful login, send people to the events dashboard
LOGIN_REDIRECT_URL  = 'events:dashboard'

# After logout, send back to the login page under accounts
LOGOUT_REDIRECT_URL = 'accounts:login'

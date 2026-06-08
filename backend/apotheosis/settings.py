"""
Configuration Django pour Apotheosis ACE.
Application de gestion de banquet pour une église.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Chemin du répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète Django (à changer en production)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-apotheosis-ace-change-in-production-2026')

# Mode debug - mettre False en production
DEBUG = True

# Hôtes autorisés
ALLOWED_HOSTS = ['*']

# Applications Django installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'banquet',
]

# Middleware (composants de traitement des requêtes)
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

# Configuration des URLs
ROOT_URLCONF = 'apotheosis.urls'

# Configuration des templates HTML
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
            ],
        },
    },
]

WSGI_APPLICATION = 'apotheosis.wsgi.application'

# Base de données SQLite intégrée à Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# Langue et fuseau horaire (Français)
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques (CSS, JS, images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise pour servir les fichiers statiques en production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Type de clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLs de connexion
LOGIN_URL = '/admin-panel/login/'
LOGIN_REDIRECT_URL = '/admin-panel/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Identifiants admin par défaut (pour le seeding)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@apotheosis.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'apotheosis2026')

# Durée de modification d'une commande en secondes (2 minutes)
ORDER_LOCK_SECONDS = 120

# Configuration des sessions
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://apotheosis-banquet.preview.emergentagent.com',
    'https://*.preview.emergentagent.com',
    'https://*.emergentcf.cloud',
    'https://*.emergentagent.com',
    'http://localhost:3000',
    'http://localhost:8000',
]

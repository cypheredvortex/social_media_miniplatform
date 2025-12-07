"""
Django settings for social_media_miniplatform project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3+wefwqs6q!kgw9y^^^0_zapldj3y9#wr5-ta3@znq$j!k=1cu'

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  # Make sure this is included
    'django.contrib.staticfiles',
    'apps.pages',
    'apps.user',
    'apps.content',
    'apps.like',
    'apps.follow',
    'apps.report',
    'apps.notification',
    'apps.enums',
    'apps.profil',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # This must come AFTER auth middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.user.middleware.SessionAuthMiddleware',  # Add our middleware
]

ROOT_URLCONF = 'social_media_miniplatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # UNCOMMENT THIS LINE
                'django.contrib.messages.context_processors.messages',  # UNCOMMENT THIS LINE
                'apps.pages.context_processors.user_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'social_media_miniplatform.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'social_media_miniplatform_db',
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        }
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (add this section)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = None

# Custom authentication backend (add this)
AUTHENTICATION_BACKENDS = [
    'apps.user.auth_backends.MongoDBAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep Django's default as fallback
]

# Custom user model (if using custom user model)
# AUTH_USER_MODEL = 'user.User'

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_NAME = 'social_media_session'
SESSION_SAVE_EVERY_REQUEST = True

# Jazzmin settings
JAZZMIN_SETTINGS = {
    "site_title": "Social Media Admin",
    "site_header": "Social Media",
    "site_brand": "Social Media",
    "welcome_sign": "Welcome to the Social Media Admin Panel",
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
}

# Login URL
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
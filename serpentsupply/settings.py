import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for security, should be changed in production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

# Debug mode (turn off in production)
DEBUG = True

# Hosts allowed to connect (empty list for development)
ALLOWED_HOSTS = ['*']

# Installed apps (includes both Django and third-party apps)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # If using Google for authentication

    'marketplace',  # Your app
    'accounts',
]

# Default site ID for allauth
SITE_ID = 1

# Authentication backends (customize for using allauth)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Middleware to handle various requests and errors
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'serpentsupply.urls'

# Template settings (load from the templates folder)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Template directory
        'APP_DIRS': True,  # Auto load templates from apps
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
WSGI_APPLICATION = 'serpentsupply.wsgi.application'

# Database settings (using SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation settings (You can add custom password validators later)
AUTH_PASSWORD_VALIDATORS = []

# Language and timezone settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'

# This tells Django where to look for static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Modify 'your_app' to the actual name of your app
]

# Automatically handle static file collection during deployment
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production use (run 'collectstatic')

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom allauth settings
ACCOUNT_LOGIN_METHOD = 'email'  # Use 'email' for login
ACCOUNT_SIGNUP_FIELDS = ['email', 'password1', 'password2']  # Fields for signup
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_REQUIRED = True  # This will be handled by 'ACCOUNT_SIGNUP_FIELDS'
ACCOUNT_USERNAME_REQUIRED = False  # Also handled by 'ACCOUNT_SIGNUP_FIELDS'

# Login and logout redirection settings
# settings.py
# settings.py

# settings.py

# settings.py

LOGIN_REDIRECT_URL = '/accounts/enter-email'  # Redirect to the 2FA email input page after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = 'account_login'

# Debugging purposes: show email verification messages in development
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Security settings (you may want to adjust these later)
CSRF_COOKIE_SECURE = False  # Only set to True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Only set to True in production with HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

#SOCIAL AUTH
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '417122981321-tef6splajpo5k368vl5gn5906k7k7mkr.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIAL_AUTH_GOOGLE_CLIENT_ID = '417122981321-tef6splajpo5k368vl5gn5906k7k7mkr.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_SECRET = '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'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '417122981321-tef6splajpo5k368vl5gn5906k7k7mkr.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mjlagunero@tip.edu.ph'
EMAIL_HOST_PASSWORD = 'tzam qkyo ugaz yhke'  # Use Gmail App Passwords, not your real password

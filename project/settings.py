"""
Django Settings for E-commerce Project
=======================================
This file contains all configuration settings for the Django project.

IMPORTANT SECURITY NOTES:
- SECRET_KEY should be changed and kept secret in production
- DEBUG should be False in production
- ALLOWED_HOSTS must be configured for production deployment

For more information:
https://docs.djangoproject.com/en/6.0/topics/settings/
"""
import os
from pathlib import Path

# ============================================================
# PATHS CONFIGURATION
# ============================================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the root directory of the project
# Example: D:\django\practice\electro\ecommerce-main\
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY SETTINGS
# ============================================================
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing (sessions, cookies, etc.)
# IMPORTANT: Change this in production and never commit to version control!
SECRET_KEY = "django-insecure-l8a_*ue&11c34%^fnft!yai0cqfzvgcx^6^)zr)vtz+agp6%or"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG mode shows detailed error pages with sensitive information
# Set to False in production!
DEBUG = True

# List of host/domain names that this Django site can serve
# IMPORTANT: Must be configured for production
# Example: ['yourdomain.com', 'www.yourdomain.com']
ALLOWED_HOSTS = []


# ============================================================
# INSTALLED APPLICATIONS
# ============================================================
# Application definition
# Each app provides specific functionality to the project

INSTALLED_APPS = [
    # Django built-in apps (admin interface, authentication, etc.)
    "django.contrib.admin",  # Admin panel at /admin/
    "django.contrib.auth",  # User authentication system
    "django.contrib.contenttypes",  # Content type framework
    "django.contrib.sessions",  # Session framework (remember logged-in users)
    "django.contrib.messages",  # Messaging framework (flash messages)
    "django.contrib.staticfiles",  # Serve static files (CSS, JS, images)
    # Custom apps for this project
    "store",  # E-commerce store app (products, cart, etc.)
    "accounts",  # User accounts app (login, register, etc.)
]


# ============================================================
# MIDDLEWARE CONFIGURATION
# ============================================================
# Middleware processes requests before they reach views
# and responses before they're sent to the browser
# Order matters! They're executed in order for requests,
# and reverse order for responses

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security enhancements
     'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently in production
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session support
    "django.middleware.common.CommonMiddleware",  # Common features
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Authentication
    "django.contrib.messages.middleware.MessageMiddleware",  # Messages
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
]


# ============================================================
# URL CONFIGURATION
# ============================================================
# Root URL configuration module
# Points to project/urls.py which contains all URL patterns
ROOT_URLCONF = "project.urls"

# Custom user model for authentication
# Instead of django.contrib.auth.models.User, use our CustomUser
# Our CustomUser uses email for login instead of username
AUTH_USER_MODEL = "accounts.CustomUser"


# ============================================================
# TEMPLATES CONFIGURATION
# ============================================================
# Configuration for Django's template engine
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Directories where Django looks for templates
        # common_templates/ contains base.html, header.html, etc.
        "DIRS": [os.path.join(BASE_DIR, "common_templates")],
        # Allow apps to have their own 'templates' folders
        # Django will look in: app_name/templates/
        "APP_DIRS": True,
        # Context processors add variables to all templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # Access 'request' in templates
                "django.contrib.auth.context_processors.auth",  # Access 'user' in templates
                "django.contrib.messages.context_processors.messages",  # Access messages
            ],
        },
    },
]


# ============================================================
# WSGI CONFIGURATION
# ============================================================
# WSGI (Web Server Gateway Interface) application
# Used when deploying with production servers like Gunicorn
WSGI_APPLICATION = "project.wsgi.application"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================
# Database settings
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Using SQLite for development (single file database)
# For production, consider PostgreSQL or MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Database type
        "NAME": BASE_DIR / "db.sqlite3",  # Database file location
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================
# Password validators ensure users create strong passwords
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # Password must not be too similar to user's other attributes
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # Password must be at least 8 characters (default)
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # Password must not be in list of common passwords
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # Password must not be entirely numeric
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================
# Settings for language, timezone, date/time formatting
# https://docs.djangoproject.com/en/6.0/topics/i18n/

# Language for the site (used in admin, error messages, etc.)
LANGUAGE_CODE = "en-us"

# Timezone for datetime storage and display
# 'UTC' is recommended for consistency
TIME_ZONE = "UTC"

# Enable internationalization (translation system)
USE_I18N = True

# Enable timezone support (store datetimes in UTC)
USE_TZ = True


# ============================================================
# STATIC FILES CONFIGURATION (CSS, JavaScript, Images)
# ============================================================
# Configuration for static files (CSS, JS, images in code)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# URL prefix for static files
# Files will be served at /static/css/style.css, etc.
STATIC_URL = "/static/"

# Directories where Django looks for static files during development
# These folders are NOT for production - use collectstatic for that
STATICFILES_DIRS = [os.path.join(BASE_DIR / "static")]  # Example: static/css/style.css

# Directory where collectstatic command collects all static files
# Run: python manage.py collectstatic
# Used for production deployment
# Static files path
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# ============================================================
# MEDIA FILES CONFIGURATION (User-uploaded files)
# ============================================================
# Configuration for media files (user uploads like product images)

# Directory where uploaded files are stored
# Example: product images go to media/products/image.jpg
MEDIA_ROOT = BASE_DIR / "media"

# URL prefix for serving media files
# Files will be accessible at /media/products/image.jpg
MEDIA_URL = "/media/"


# ============================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================================
# Specifies the default type for auto-created primary key fields
# BigAutoField: 64-bit integer (supports up to 9 quintillion records)
# AutoField: 32-bit integer (supports up to 2 billion records)
# New in Django 3.2+
# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# AUTHENTICATION SETTINGS
# ============================================================
# URL to redirect users to when they need to log in
# Used by @login_required decorator
LOGIN_URL = "/accounts/login/"

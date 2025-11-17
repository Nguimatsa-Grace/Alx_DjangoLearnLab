from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-m_k8i(v0t+3w%3a^@b0v3p8*s53y_e*a^3k6g3-d-2s8r5-h$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'core_security',
    
    # --- TWO-FACTOR AUTHENTICATION APPS ---
    'two_factor',
    'django_otp',
    'django_otp.plugins.otp_totp',
    # ------------------------------------
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf', # CRITICAL: This is the app containing the CustomUser model
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_config.urls' 

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

WSGI_APPLICATION = 'core_config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =======================================================
# --- CUSTOM USER MODEL & MEDIA CONFIGURATION (CRITICAL) ---
# =======================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =======================================================
# --- TWO-FACTOR AUTHENTICATION (2FA) CONFIGURATION (CRITICAL) ---
# =======================================================
AUTHENTICATION_BACKENDS = [
    'two_factor.backends.TwoFactorBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'security_home' 
TWO_FACTOR_CUSTOM_MODEL = 'bookshelf.CustomUser'
SILENCED_SYSTEM_CHECKS = ["urls.E004"] 

# Configure Django to use the CustomUser model for authentication
# CRITICAL: This line defines the custom user model location
AUTH_USER_MODEL = 'bookshelf.CustomUser'
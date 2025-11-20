# LibraryProject/LibraryProject/settings.py

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m_e#5p*5x@h*^2*@+y_1*@*8@2e*c@t9r+9*c@i5r@f#@x%i&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # 🚨 Set DEBUG to False (Required for security check)

# For testing in a production mode locally, we allow all hosts.
ALLOWED_HOSTS = ['*'] # Required for DEBUG=False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your Project Apps
    'bookshelf',
    'users',
    'relationship_app',
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

# 🚨 CRITICAL FIX: Update to the new directory name (LibraryProject instead of config)
ROOT_URLCONF = 'LibraryProject.project_urls_fixed'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'LibraryProject.wsgi.application' # Also update WSGI

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


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

# Custom User Model and Login URLs
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/admin/login/' 
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (for user uploads like profile pictures)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# Security Configuration (Required Settings)
# ==============================================================================

# Protects against XSS by enabling the browser's built-in XSS filter.
SECURE_BROWSER_XSS_FILTER = True 

# Prevents the browser from MIME-sniffing content type, reducing XSS risk.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Protects against Clickjacking attacks by setting the X-Frame-Options header.
X_FRAME_OPTIONS = 'DENY' 

# Ensures the CSRF cookie is only sent over HTTPS (requires HTTPS in production).
CSRF_COOKIE_SECURE = True 

# Ensures the Session cookie is only sent over HTTPS (requires HTTPS in production).
SESSION_COOKIE_SECURE = True 

# ==============================================================================
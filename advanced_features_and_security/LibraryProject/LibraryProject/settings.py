# LibraryProject/LibraryProject/settings.py

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m_e#5p*5x@h*^2*@+y_1*@*8@2e*c@t9r+9*c@i5r@f#@x%i&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Must be False for production and security settings to be fully effective

# Required for DEBUG=False
ALLOWED_HOSTS = ['*']


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
    # SecurityMiddleware should be at the top
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Update to the new directory name (LibraryProject instead of config)
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

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


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
# 🚨 TASK 3: HTTPS and Secure Redirect Configuration
# ==============================================================================

# Step 1: Configure Django for HTTPS Support
# SECURE_SSL_REDIRECT = True ensures all non-HTTPS requests are redirected to HTTPS.
# NOTE: This setting requires your web server (Nginx/Apache) to be configured for SSL.
SECURE_SSL_REDIRECT = True 

# SECURE_HSTS_SECONDS enables HTTP Strict Transport Security (HSTS). 
# This tells browsers (for 1 year, 31536000 seconds) to only access the site via HTTPS.
SECURE_HSTS_SECONDS = 31536000

# SECURE_HSTS_INCLUDE_SUBDOMAINS applies the HSTS policy to all subdomains.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_HSTS_PRELOAD allows the site to be submitted to browser HSTS preload lists.
SECURE_HSTS_PRELOAD = True

# Step 2: Enforce Secure Cookies (Already set in Task 2, confirmed here)
# CSRF_COOKIE_SECURE ensures the CSRF token is only sent over HTTPS.
CSRF_COOKIE_SECURE = True 

# SESSION_COOKIE_SECURE ensures the session cookie is only sent over HTTPS.
SESSION_COOKIE_SECURE = True 

# Step 3: Implement Secure Headers (Already set in Task 2, confirmed here)
# SECURE_BROWSER_XSS_FILTER enables the browser's built-in XSS filter.
SECURE_BROWSER_XSS_FILTER = True 

# SECURE_CONTENT_TYPE_NOSNIFF prevents browsers from MIME-sniffing (protects against XSS).
SECURE_CONTENT_TYPE_NOSNIFF = True

# X_FRAME_OPTIONS prevents the site from being embedded in an iframe (Clickjacking protection).
X_FRAME_OPTIONS = 'DENY' 

# ==============================================================================
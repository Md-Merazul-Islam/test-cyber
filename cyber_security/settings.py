
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
import os
from datetime import timedelta
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']  # Allow host

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Required by allauth
    'django.contrib.sites',

    # Third-party apps
    'rest_framework',
    'corsheaders',

    # Django Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # for s3 storage
    'storages',

    # Local apps
    'auths',  # auths app
    'services',  # services app
    'reviews',  # views app
    'teams',  # teams app
    'contracts',  # contracts app
    'bookings',  # bookings app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Required for django-allauth
    "allauth.account.middleware.AccountMiddleware",

    "corsheaders.middleware.CorsMiddleware",  # corse headers middleware
]

ROOT_URLCONF = 'cyber_security.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
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

WSGI_APPLICATION = 'cyber_security.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Media files configuration (e.g., images, videos)
MEDIA_URL = '/media/'  # URL endpoint to access media files via web
# Where the files are stored (on the file system)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files configuration (for JS, CSS, etc.)
STATIC_URL = '/static/'  # URL endpoint to access static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # Where static files are stored

# Media File storage settings - use BinaryField to store files in the database
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)
# STATIC_URL = 'static/'


# extra settings add from me --------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": "your-google-client-id",
            "secret": "your-google-client-secret",
            "key": "",
        }
    }
}


CORS_ALLOW_ALL_ORIGINS = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTH_USER_MODEL = 'auths.CustomUser'

SESSION_COOKIE_AGE = 3600  # 1 hour in seconds


# ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True


# corse
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5500',
    'http://127.0.0.1:5501',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://*.127.0.0.1',


]

CSRF_TRUSTED_ORIGINS = [

    'https://*.127.0.0.1',
    'http://localhost:8000',
    'http://127.0.0.1:5500',
    'http://127.0.0.1:5501',
    'http://127.0.0.1:8000',
]


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
    'OPTIONS'
]


# --- Email  Backend --------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# ------.env start  ---------------------------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True

# for email notification
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# for google auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = "http://127.0.0.1:8000/api/v1/auth/google/callback/"

# ------.env end  ----------------------------------------------------------------------------------------


# DATABASES = {
#     'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
# }

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',  # Refers to the PostgreSQL container name in Docker Compose
        'PORT': '5432',  # Default PostgreSQL port
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DigitalOcean Spaces (similar to AWS S3).----------------------------------------------------------------

# Default File Storage to use S3-Compatible Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DigitalOcean Spaces Credentials
# AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

# AWS_S3_ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"
# AWS_ACCESS_KEY_ID="DO002RGDJ947DJHJ9WDT"
# AWS_SECRET_ACCESS_KEY="e5+/pko6Ojar51Hb8ojUKfq2HtXy+tnGKOfs3rIcEfo"
# AWS_STORAGE_BUCKET_NAME="smtech-space"

AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
AWS_ACCESS_KEY_ID = "DO002RGDJ947DJHJ9WDT"
AWS_SECRET_ACCESS_KEY = "e5+/pko6Ojar51Hb8ojUKfq2HtXy+tnGKOfs3rIcEfo"
AWS_STORAGE_BUCKET_NAME = "smtech-space"

# Set permissions
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.nyc3.cdn.digitaloceanspaces.com"

# Media Files Configuration
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

# AWS_DEFAULT_ACL = "public-read"
AWS_DEFAULT_ACL = None  # Prevents permission issues
AWS_QUERYSTRING_AUTH = False  # Allows files to be accessed without signed URLs
AWS_S3_FILE_OVERWRITE = False

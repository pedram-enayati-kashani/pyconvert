import environ
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
)

# Read .env file
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

SERVE_STATIC_LOCAL = env.bool("SERVE_STATIC_LOCAL", default=False)

# site config
SITE_MODE = env('SITE_MODE')
ORGANIZATION_NAME = env('ORGANIZATION_NAME')

WSGI_APPLICATION = 'config.wsgi.application'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # Apps
    'Client',
    'App_panel',
    'Admin_panel',
    'module',
    # Third party
    'django_render_partial',
    'django_ckeditor_5',
    'sorl.thumbnail',
    'captcha',
    'django_vite',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'Admin_panel.middleware.smart_i18n.SmartUrlLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'Client.middleware.Redirect.RedirectMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'Client.middleware.Maintenance.MaintenanceMiddleware',
    'Client.middleware.head_request.CKEditorMetadataMiddleware',
    'Admin_panel.middleware.AdminRoutesStatusMiddleware',
    'Admin_panel.middleware.Modules.ModuleRoutesStatusMiddleware',
    'App_panel.middleware.Auth.SuperAdminAccessRoutesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Custom User Model
AUTH_USER_MODEL = 'App_panel.Users'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

AUTHENTICATION_BACKENDS = [
    'Admin_panel.helpers.Auth.UsernameOrEmailBackend',
]


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = "fa"

LANGUAGES = [
    ("fa", _("فارسی")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = env('TIME_ZONE')
USE_I18N = env.bool('USE_I18N')
USE_L10N = env.bool('USE_L10N')
USE_TZ = env.bool('USE_TZ')

# Static files (CSS, JavaScript, Images)
STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')

# ============================================
# Cache Settings (Redis)
# ============================================
REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_DB = env.int("REDIS_DB", default=0)
REDIS_KEY_PREFIX = env("KEY_PREFIX")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env(
            "REDIS_URL",
            default=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": env("KEY_PREFIX",),
        "TIMEOUT": env.int("CACHE_TTL", default=300),
    }
}




# ============================================
#  SITE Settings
# ============================================

SITE_ID = 1


# ============================================
# Session & Security Settings (Dynamic)
# ============================================

SESSION_COOKIE_AGE = 86400  # 24H
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# Security Middleware Settings (برای Production)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)

# تنظیم هدر پروکسی برای Nginx
proxy_header = env('SECURE_PROXY_SSL_HEADER', default='HTTP_X_FORWARDED_PROTO,https').split(',')
SECURE_PROXY_SSL_HEADER = (proxy_header[0], proxy_header[1])

SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF')
SECURE_BROWSER_XSS_FILTER = env.bool('SECURE_BROWSER_XSS_FILTER')
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')

# ============================================
# Logging
# ============================================
LOG_LEVEL = env('LOG_LEVEL')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}

# ============================================
# CKEDITOR_5 Configuration
# (این بخش چون کانفیگ پیچیده است، در settings.py می‌ماند)
# ============================================
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'imageUpload',],
        # تنظیمات دیگر...
    },
}

CKEDITOR_5_FILE_STORAGE = "Client.helpers.storage.CKEditorStorage"

# ============================================
# Email Settings
# ============================================
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# ============================================
# Thumbnail Settings
# ============================================

THUMBNAIL_CACHE = 'default'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'
THUMBNAIL_PREFIX = 'cache/'
THUMBNAIL_BACKEND = 'sorl.thumbnail.base.ThumbnailBackend'
THUMBNAIL_ENGINE="Admin_panel.helpers.thumbnail_engine.WatermarkEngine"

# ============================================
# DJANGO VITE Settings
# ============================================
VITE_PROTOCOL = env.str("VITE_DEV_PROTOCOL", default="http")

MANIFEST_FILE = BASE_DIR / "static" / "dist" / ".vite" / "manifest.json"
if not MANIFEST_FILE.exists():
    MANIFEST_FILE = BASE_DIR / "static" / "dist" / "manifest.json"

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "dev_server_protocol": VITE_PROTOCOL,
        "dev_server_host": env.str("VITE_DEV_HOST", default="192.168.10.103"),
        "dev_server_port": env.int("VITE_DEV_PORT", default=5173),
        "static_url_prefix": "" if DEBUG else "dist",
        "manifest_path": MANIFEST_FILE,
    }
}


# ============================================
# CAPTCHA Settings
# ============================================
CAPTCHA_FONT_SIZE = 30
CAPTCHA_IMAGE_SIZE = (200, 60)
CAPTCHA_LENGTH = 5
CAPTCHA_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_arcs',
    # 'captcha.helpers.noise_dots',
)


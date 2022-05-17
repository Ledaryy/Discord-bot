
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent



import os

# Django
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEBUG = int(os.environ.get("DEBUG", default=0))
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

# Deployment
WORK_CHANNEL_ID = os.environ.get("WORK_CHANNEL_ID")
BUMP_CHANNEL_ID = os.environ.get("BUMP_CHANNEL_ID")
ANIHOUSE_BOT_ID = os.environ.get("ANIHOUSE_BOT_ID")
BOT_NAME_TAG = os.environ.get("BOT_NAME_TAG")

BUMP_NAMES = {
    "UP": "S.up",
    "BUMP": "Bump",
    "LIKE": "Like"
}

BUMP_COMMANDS = {
    "UP": "!up",
    "BUMP": "!bump",
    "LIKE": "!like"
}

COMMANDS_ENABLED = ["LIKE"]

LOGGER_FORMAT = "[%(asctime)s] :: %(levelname)s :: %(filename)s :: %(funcName)s :: %(lineno)s :: %(message)s"

# CELERY STUFF
BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'

# Application definition

INSTALLED_APPS = [
    'backend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'webhost.urls'

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

WSGI_APPLICATION = 'webhost.wsgi.application'

# Database =====================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bodytrakn",
        "USER": "iamin",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": 5432,
    }
}

DATABASES["default"] = dj_database_url.parse(
    os.environ["POSTGRES_LOCAL_CONN"], conn_max_age=600, ssl_require=False
)


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



STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

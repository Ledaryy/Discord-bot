
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


ALLOWED_HOSTS = []

import os
from dotenv import load_dotenv

load_dotenv()

#TOKEN = os.environ['TOKEN']
SECRET_KEY = os.environ['SECRET_KEY']
WORK_CHANNEL_ID = os.environ['WORK_CHANNEL_ID']
BUMP_CHANNEL_ID = os.environ['BUMP_CHANNEL_ID']
ANIHOUSE_BOT_ID = os.environ['ANIHOUSE_BOT_ID']
BOT_NAME_TAG = os.environ['BOT_NAME_TAG']
PRODUCTION = True if os.environ['PRODUCTION'] else False
DEBUG = True if os.environ['DEBUG'] else False

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

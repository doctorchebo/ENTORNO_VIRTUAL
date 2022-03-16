"""
Django settings for CRUD project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import dj_database_url
from celery.schedules import crontab
from decouple import config
from pathlib import Path
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if settings.DEBUG:
    SECRET_KEY = config('SECRET_KEY')
else:
    SECRET_KET = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# if setting.DEBUG:
#     DEBUG = config('DEBUG', cast=bool, default=True)
# else:
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'custodia-bmsc.herokuapp.com'] 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'rest_framework',
    'django_filters',
    'custodia',
    'members',
    'dashboard',
    'crispy_forms',
    'bootstrap_datepicker_plus',
    'fontawesomefree',
    'import_export',
    # PART OF DASH
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'dpd_static_support',
    # 'debug_toolbar',
    'auditlog',
    'django_celery_beat',
    'dbbackup',
]

# DB BACKUP
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'backup'}

# REDIS URL
if setting.DEBUG == False:
    REDIS_URL = os.environ['REDIS_URL']

# CELERY SETTINGS
if settings.DEBUG:
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
else:
    CELERY_BROKER_URL = REDIS_URL


CELERY_TIMEZONE = 'America/Santo_Domingo'
CELERY_BEAT_SCHEDULE = {
    'run-every-monday': {
        'task': 'custodia.tasks.enviar_emails_task',
        'schedule': crontab(hour=6, minute=30),
        'args': (),
    },
    'run-every-sunday': {
        'task': 'custodia.tasks.copiar_base_datos',
        'schedule': crontab(hour=11, minute=30, day_of_week=1),
        'args': (),
    },
}

if settings.DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND':'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'TIMEOUT': 5*60,
        }
    }


CRISPY_TEMPLATE_PACK = 'bootstrap4'

BOOTSTRAP4 = {
    'include_jquery': True,
}

LOGIN_URL = '/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WHITE NOISE (SERVE STATIC FILES WITHOUT OTHER SERVERS E.G. NGINX)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    

    'django.middleware.csrf.CsrfViewMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # DEBUG TOOLBAR
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # DASH MIDDLEWARE (IF THERE ARE HEADER AND FOOTER)
    'django_plotly_dash.middleware.BaseMiddleware',
    # DASH MIDDLEWARE (IF ASSETS ARE SERVED LOCALLY)
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'CRUD.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'CRUD.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if settings.DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'custodia',
            'USER': 'root',
            'PASSWORD': config('BD_PASSWORD'),
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config()
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Santo_Domingo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR,'static') 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media') 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
    os.path.join(BASE_DIR,'media')
]



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if settings.DEBUG:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'marcelo.munoz.coaquira@gmail.com'
    EMAIL_HOST_PASSWORD = 'fvgbcpdurevgykwe'
    EMAIL_PORT = '587'
# DEFAULT_FROM_EMAIL = 'custodia@bmsc.com'
    EMAIL_USE_TLS =True
    EMAIL_USE_SSL = False
else:
    EMAIL_HOST = os.environ[MAILGUN_SMTP_SERVER]
    EMAIL_HOST_USER = os.environ[MAILGUN_SMTP_LOGIN]
    EMAIL_HOST_PASSWORD = os.environ[MAILGUN_SMTP_PASSWORD]
    EMAIL_PORT = os.environ[MAILGUN_SMTP_PORT]

#IMPORT-EXPORT CONFIG
IMPORT_EXPORT_USE_TRANSACTIONS = True


# DEBUG TOOLBAR CONFIG
INTERNAL_IPS = [
    "127.0.0.1",
]

DATE_FORMAT = "d/m/Y"
# DATE_INPUT_FORMATS = ('%Y-%m-%d')
USE_L10N = False

# DJANGO DASH CONFIGURATION -----------------------------------------------------
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Adding ASGI Application
# ASGI_APPLICATION = 'django_dash.routing.application'
#
# To use home.html as default home page
# LOGIN_REDIRECT_URL = ‘home’
# LOGOUT_REDIRECT_URL = ‘home’

PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
    "ws_route" :   "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
    "insert_demo_migrations" : False,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,
}
# Staticfiles finders for locating dash app assets and related files

STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

# Plotly components containing static content that should
# be handled by the Django staticfiles infrastructure

PLOTLY_COMPONENTS = [

    # Common components
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    # django-plotly-dash components
    'dpd_components',
    # static support if serving local assets
    'dpd_static_support',

    # Other components, as needed
    'dash_bootstrap_components',
]


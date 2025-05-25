from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ot2yxq)jpk!*99k2!w++fw!%bt!vm(jre5jer+e=#q#s*=_qqs'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'corsheaders',
    'rest_framework',
    'drf_yasg',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4321",  
]

ROOT_URLCONF = 'noticiero.urls'

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

WSGI_APPLICATION = 'noticiero.wsgi.application'


'''
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'noticiero',  # Nombre de tu base de datos en MongoDB
        'CLIENT': {
            'host': 'mongodb://localhost:27017',  # Ajusta según tu configuración
        }
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'noticiero_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb',
            'port': 27017,
        }
    }
}


from mongoengine import connect

connect(
    db='noticiero_db',
    host='mongodb',
    port=27017
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

'''
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.CustomJWTAuthentication.CustomJWTAuthentication',
    ],
}
'''

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = ['noticiero-api', 'localhost', '127.0.0.1', '0.0.0.0','http://localhost:4321', 'http://localhost:8000']
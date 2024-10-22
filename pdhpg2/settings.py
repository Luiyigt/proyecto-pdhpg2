from pathlib import Path
import os




CSRF_TRUSTED_ORIGINS = ['https://proyecto-pdhpg2.onrender.com']

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%ra=x=d3*16td%mk6#bh!b(!!-75f^zzxbaoq)fon(@p-cyf12'
DEBUG = True
SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ['proyecto-pdhpg2.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'resoluciones',
    'django_extensions',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

SITE_ID = 1
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Añadir WhiteNoise aquí
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'pdhpg2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'pdhpg2.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'pdhpg2'),  # Coloca el nombre correcto
        'USER': os.environ.get('DB_USER', 'pdhpg2_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'EtAjwi3q6YGFA78syH9SwvwCrzfjrN59'),
        'HOST': os.environ.get('DB_HOST', 'dpg-cs72oe56l47c73900hag-a'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


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
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Añade esto si no está configurado
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = ''
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'lista_resoluciones'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'luismazariegos318@gmail.com'
EMAIL_HOST_PASSWORD = 'khribhzfhczdjzib'
DEFAULT_FROM_EMAIL = 'luiyimaza@gmail.com'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SECURE_SSL_REDIRECT = False
DEFAULT_FROM_EMAIL = 'luismazariegos318@gmail.com'
SERVER_EMAIL = 'luismazariegos318@gmail.com'
EMAIL_SUBJECT_PREFIX = '[PDH SOLOLA 2024] '

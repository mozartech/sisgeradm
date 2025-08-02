import os
from pathlib import Path

import environ

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    MEDIAFILES_STORAGE=(str, ''),
    DEBUG=(bool, False),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
file_env = os.path.join(BASE_DIR, '.env')

if Path(file_env).is_file():
    environ.Env.read_env(file_env)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # extras apps
    'widget_tweaks',
    # django-allauth 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # apps
    'accounts',
    'base',
    'comercial',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    #"allauth.account.middleware.AccountMiddleware",    
]

ROOT_URLCONF = 'sisgeradm.urls'

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
                # contexto para a versao do educatize
                'base.context_version.educatize_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'sisgeradm.wsgi.application'

# django-allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}

AUTH_USER_MODEL = 'accounts.MyUser'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Languages using BiDi (right-to-left) layout

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'static'),
]

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    #AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
    #AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    #AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    #AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    #AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)
    #AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    #AWS_S3_SIGNATURE_VERSION = 's3v4'
    #AWS_DEFAULT_ACL = None # 
    # s3 media settings
    DEFAULT_FILE_STORAGE = 'core.storages.MediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

ACCOUNT_AUTHENTICATION_METHOD = "email"

# Controla o tempo de vida da sessão.
# Defina como None (default) para perguntar ao usuário (“Lembra de mim?”),
# False para não lembrar e True para lembrar sempre.
ACCOUNT_SESSION_REMEMBER = True

# Ao se cadastrar, deixe o usuário digitar a senha duas vezes para evitar erros de digitação
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

#ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# Determina se o usuário será desconectado automaticamente ou não por uma solicitação GET.
# GET não foi projetado para modificar o estado do servidor e, neste caso, pode ser perigoso.
# Consulte LogoutView na documentação para obter detalhes.
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_LOGOUT_REDIRECT_URL = '/logout'

# Determina se o usuário será desconectado automaticamente após alterar ou definir sua senha.
# Veja a documentação para invalidação de sessão do Django na alteração de senha.
# ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
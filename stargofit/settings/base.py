"""
Django settings for stargofit_fourth project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    os.path.join(__file__, os.pardir))))  # pointing to parent dir with pardir

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'abb97b75-ffa4-45c3-ad94-ad891bd8165a'


ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'b65b4809.ngrok.io']

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    # Add your apps here to enable them

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'modeltranslation',
    'training_plans.apps.Training_plansConfig',
    'embed_video',
    'memcache_status',
    'rest_framework',
    'social_django',
    'sorl.thumbnail',
    'debug_panel',
    'django_countries',
    'multiselectfield',
    'rosetta',
    'nested_inline',
]


LANGUAGES = (
    ('de', _('Deutsch')),
    ('en', _('Englisch')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'de'

MODELTRANSLATION_TRANSLATION_FILES = (
    'training_plans.translation',
)

USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_SESSION_KEY = 'de'
LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly']
}

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # UpdateMiddleware before CommonMiddleware becouse it runs during response time
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # FetchFrom... after Common becouse it needs to access request data set by the latter (letztere)
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


MIDDLEWARE_CLASSES = (
    'debug_panel.middleware.DebugPanelMiddleware',
)


ROOT_URLCONF = 'stargofit.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['C:/Users/paul-/OneDrive/Desktop/django/stargofit/stargofit/templates',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/training_plans/templates/fitness/exercises/list',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/training_plans/templates/fitness',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/account/templates/base',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/training_plans/templates/fitness/exercises/endurance_training',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/training_plans/templates/fitness/flexibility_training',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/training_plans/templates/fitness/exercises/aerobic',
                 'C:/Users/paul-/OneDrive/Desktop/django/stargofit/training_plans/templates/fitness/exercises/strngth_training', ],
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


WSGI_APPLICATION = 'stargofit.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_COOKIE_NAME = 'django_language'

LANGUAGE_COOKIE_AGE = None

LANGUAGE_COOKIE_DOMAIN = None

LANGUAGE_COOKIE_PATH = '/'

LANGUAGE_COOKIE_SECURE = False

LANGUAGE_COOKIE_HTTPONLY = False

LANGUAGE_COOKIE_SAMESITE = None


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
LOCAL_STATIC_FILES_PATH = os.path.join(BASE_DIR, 'static_files')

STATICFILES_DIRS = [os.path.join(LOCAL_STATIC_FILES_PATH, 'static')]


# redirect the user to this url after log-in:
LOGOUT_URL = 'logout'  # URL redirect the user to logout


# for uploaded content -> serving it with development server
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(LOCAL_STATIC_FILES_PATH, 'media')


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# for writing emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = [
    # kept default that is used to authenticate with username + password
    'django.contrib.auth.backends.ModelBackend',
    # include e-mail based authentication
    'account.authentication.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',  # login with facebook account
    'social_core.backends.twitter.TwitterOAuth',  # login with twitter
    'social_core.backends.google.GoogleOAuth2',  # login with google
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = '448994255868751'  # facebook App ID
SOCIAL_AUTH_FACEBOOK_SECERET = 'c9feb07fc5b796c88e1a9ae476161e80'
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email'] # for permission to ask for users email

SOCIAL_AUTH_TWITTER_KEY = 'Gtf0nHV5oGu56z3ae7isDHkqn'
SOCIAL_AUTH_TWITTER_SECERET = 'wpvt9tuY4gCDO5f8qXd8EevUUMbJqk0M0fWViYSnRMRq3ZK9Wi'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'oR6yQZp2HtJZLEDhjIWsahSy'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECERET = '850897429719-42d3l4v3rm6ht6mu9t92svlj5a9uma3s.apps.googleusercontent.com'

# for thumbnail customizing
THUMBNAIL_DEBUG = True


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

SESSION_COOKIE_DOMAIN = None


AUTH_USER_MODEL = 'account.Member'

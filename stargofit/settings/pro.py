# settings for production environment

from .base import *

# mandatory (verpflichtend) for any production env
DEBUG = True

# if view raises an exception, all information will be sent to admins per email
#ADMINS = (
#    ('Paul Hornig', 'paul-hornig@gmx.de'),
#    )

# allow hosts included in this list to server the app
#ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stargofit',
        'USER': 'postgres',
        'PASSWORD': '',
        'PORT': '5432',
        'HOST': 'localhost'
}
}


import json

from .base import *

DEV_JSON = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DEV_JSON['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = DEV_JSON['DATABASES']

WSGI_APPLICATION = 'config.wsgi.dev.application'

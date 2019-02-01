import json

from .base import *

PRODUCTION_JSON = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = PRODUCTION_JSON['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# CORS ALLOW WHITELIST
CORS_ORIGIN_WHITELIST = (
    # 추후에 추가될 Front 도메인
)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = PRODUCTION_JSON['DATABASES']

WSGI_APPLICATION = 'config.wsgi.production.application'

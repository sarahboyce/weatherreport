"""
Django local settings for weatherreport project.

This file contains settings unsuitable for production
Please see production.py as an example file for a production deployment
"""
from .common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

TEMPLATES[0]["OPTIONS"]["debug"] = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "weatherreport",
        "USER": "postgres",
        "PASSWORD": "a",
        "HOST": "localhost",
        "PORT": "5432",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cachetable",
        "KEY_PREFIX": "local",
    }
}

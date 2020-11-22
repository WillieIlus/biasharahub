import os

from django.core.exceptions import ImproperlyConfigured

from .settings import BASE_DIR

SECRET_KEY = os.environ.get("CR_SECRET_KEY") or ImproperlyConfigured("CR_SECRET_KEY not set")

DEBUG = False

hosts = os.environ.get("CR_HOSTS") or ImproperlyConfigured("CR_HOSTS not set")

try:
    ALLOWED_HOSTS = hosts.split(",")
except:
    raise ImproperlyConfigured("CR_HOSTS could not be parsed")

if os.environ.get("CR_USESQLITE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    name = os.environ.get("CR_DB_NAME") or ImproperlyConfigured("CR_DB_NAME not set")
    user = os.environ.get("CR_DB_USER") or ImproperlyConfigured("CR_DB_USER not set")
    password = os.environ.get("CR_DB_PASSWORD") or ImproperlyConfigured("CR_DB_PASSWORD not set")
    host = os.environ.get("CR_DB_HOST") or ImproperlyConfigured("CR_DB_HOST not set")
    port = os.environ.get("CR_DB_PORT") or ImproperlyConfigured("CR_DB_PORT not set")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
    }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'



import os

from .settings import BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4-#uonxctis^jk88-&&%s4gci7=0xvp66y4^4nmrtmsp6=i_=%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '0.0.0.0', '127.0.0.1', 'biasharahub.com', 'www.biasharahub.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
         "NAME": 'biasharahubdb',
            "USER": 'postgres',
            "PASSWORD": 'tungsten1',
            "HOST": '127.0.0.1',
            "PORT": '5432',
    }
}



STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = "http://127.0.0.1:8000/media/"

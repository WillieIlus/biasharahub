"""
WSGI config for biasharahub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

# from biasharahub import MyWSGIApp
#
# application = MyWSGIApp()
# application = WhiteNoise(application, root='/path/to/static/files')
# application.add_files('/path/to/more/static/files', prefix='more-files/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biasharahub.settings")

application = get_wsgi_application()

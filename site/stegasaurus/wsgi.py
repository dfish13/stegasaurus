"""
WSGI config for stegasaurus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_DIR, '..', 'steganographyenv/lib/python3.5/site-packages'))
sys.path.insert(1, PROJECT_DIR)
sys.path.insert(2, os.path.join(PROJECT_DIR, '..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stegasaurus.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

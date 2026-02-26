"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

app = application  # For compatibility with some WSGI servers

# On Vercel, /tmp/ is ephemeral — run migrations on cold start to create tables
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    import django
    django.setup()
    call_command('migrate', '--run-syncdb', verbosity=0)
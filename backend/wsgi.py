import os
import sys

sys.path.insert(0, '/app/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apotheosis.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

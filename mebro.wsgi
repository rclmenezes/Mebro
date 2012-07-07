import os, sys
path = '/srv/mebro'

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


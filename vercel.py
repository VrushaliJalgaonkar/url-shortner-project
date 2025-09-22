from django.core.wsgi import get_wsgi_application

# Vercel needs this callable to handle requests
application = get_wsgi_application()

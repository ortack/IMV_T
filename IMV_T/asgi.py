"""
ASGI config for IMV_T project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IMV_T.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)) # URLRouter(ws_urlpatterns) # URLRouter([
    # Just HTTP for now. (We can add other protocols later.)
})

# Configuraci�n de depuraci�n solo si DEBUG est� configurado en True
if os.environ.get("DEBUG", ""):
    channel_layer = get_channel_layer()
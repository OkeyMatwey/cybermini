import os

import django
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from kibermini_nodes import consumers as c1
from kibermini_web import consumers as c2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kibermini.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                url(r"^nodes/$", c1.NodeConsumer.as_asgi()),
                url(r"^users/$", c2.UserConsumer.as_asgi()),
            ]
        )
    ),
})
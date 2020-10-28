from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from kibermini_nodes import consumers as c1
from kibermini_web import consumers as c2


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                url(r"^nodes/$", c1.NodeConsumer),
                url(r"^users/$", c2.UserConsumer),
            ]
        )
    ),
})
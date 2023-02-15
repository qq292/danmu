import attr
from django.urls import path

from BulletScreen import consumers

websocket_urlpatterns = [
    path('ws/s/', consumers.BulletScreenConsumer.as_asgi()),
]
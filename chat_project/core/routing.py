from django.urls import path,re_path
from . import consumer

websocket_urlpatterns = [
    path('connect/<str:room_slug>', consumer.ChatConsumer.as_asgi()),
]
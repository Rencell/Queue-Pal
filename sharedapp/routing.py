from django.contrib import admin
from django.urls import path
from staff import views
from sharedapp.consumers import consumer,adduserconsumer

websocket_urlpatterns = [
    path('ws/chat/<str:code>/', consumer.QueueConsumer.as_asgi()),
    path('ws/staff_room/', adduserconsumer.NewqueueConsumer.as_asgi())
]

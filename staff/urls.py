from django.contrib import admin
from django.urls import path,include
from staff import views


urlpatterns = [
    path('', views.user_index.as_view(), name="staff_index"),
    path('<str:code>', views.room_view.as_view(), name="staff_queue_room"),
]

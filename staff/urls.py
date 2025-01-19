from django.contrib import admin
from django.urls import path,include
from staff import views


urlpatterns = [
    path('', views.user_index.as_view(), name="staff_index"),
    path('<str:code>', views.room_view.as_view(), name="staff_queue_room"),
    path('<str:code>/create', views.store_customer.as_view(), name="staff_create_customer"),
    path('<str:code>/<int:pk>/delete', views.destroy_customer.as_view(), name="staff_delete_customer"),
]

htmxpattern = [
    path('timer/', views.htmxtry, name="staff_timer"),
]

urlpatterns += htmxpattern
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
    path('timer/<int:userroom_id>', views.htmxtry, name="staff_timer"),
    path('appointing/<int:userroom_id>', views.appoint_user, name="staff_appoint"),
    path('noshow/<int:userroom_id>', views.noshow_user, name="staff_noshow"),
]

urlpatterns += htmxpattern
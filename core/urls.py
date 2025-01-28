
from django.urls import path,include
from core import views

urlpatterns = [
    path('', views.index.as_view(), name="core_index"),
    path('issue/<str:code>/', views.issue_view.as_view(), name="core_issue"),
    path('onQueue/', views.queue_view.as_view(), name="core_queue"),
    path('onQueue/unidentified', views.queue_error.as_view(), name="core_queue_error"),
    path('cancelled/', views.closing_view.as_view(), name="core_cancelled"),
]

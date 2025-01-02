
from django.urls import path,include
from Accounts import views
urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path('', include('django.contrib.auth.urls')),
]

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('staff/', include('staff.urls')),
    path('', include('Accounts.urls')),
    path('webpush/', include('webpush.urls')),
]

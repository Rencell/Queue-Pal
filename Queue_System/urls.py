
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

class index(TemplateView):
    template_name="index.html"
class about(TemplateView):
    template_name="index_sub/about.html"


urlpatterns = [
    path('', index.as_view(), name="index"),
    path('about/', about.as_view(), name="about"),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('staff/', include('staff.urls')),
    path('', include('Accounts.urls')),
]

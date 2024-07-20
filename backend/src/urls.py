"""
URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

prefix = 'api/aviv/'
urlpatterns = [
    path(prefix + 'admin/', admin.site.urls),
    path(prefix + 'llm/', include('llm.urls')),
    path(prefix + 'user/', include('user.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

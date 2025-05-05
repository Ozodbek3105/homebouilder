from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin paneli uchun yo‘l
    path('', include('main.urls')),  # `main` ilovasining URL’lari
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
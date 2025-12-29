from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('', include('courses.urls')),
    path('accounts/', include('allauth.urls')),  # Allauth URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# This allows image uploads to work during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

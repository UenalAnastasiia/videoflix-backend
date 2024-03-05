from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from video.views import export_backend_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('export/', export_backend_view),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
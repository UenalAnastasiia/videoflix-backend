from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from category.views import CategoryViewSet
from login.views import LoginView
from video.views import VideoViewSet, export_backend_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('export/', export_backend_view),
    path('videos/', VideoViewSet.as_view()),
    path('category/', CategoryViewSet.as_view()),
    path('login/', LoginView.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
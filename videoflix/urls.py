from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from category.views import CategoryDetailsViewSet, CategoryViewSet
from login.views import LoginView
from registration.views import RegisterView
from video.views import VideoDetailsViewSet, VideoViewSet, export_backend_view
from video_list.views import ListDetailsViewSet, ListViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('export/', export_backend_view),
    path('videos/', VideoViewSet.as_view()),
    path('videos/<int:pk>/', VideoDetailsViewSet.as_view()),
    path('category/', CategoryViewSet.as_view()),
    path('category/<int:pk>/', CategoryDetailsViewSet.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('list/', ListViewSet.as_view()),
    path('list/<int:pk>/', ListDetailsViewSet.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
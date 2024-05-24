from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from user.views import LoginView, LogoutView, UserDetailsViewSet, UsersViewSet, register_view, confirm_email_view
from category.views import CategoryDetailsViewSet, CategoryViewSet, UserCategories
from video.views import UserUploads, VideoDetailsViewSet, VideoViewSet, export_backend_view
from video_list.views import ListDetailsViewSet, ListViewSet
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('export/', export_backend_view),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('confirm_email/<token>/', confirm_email_view, name='confirm-email'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('users/', UsersViewSet.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailsViewSet.as_view(), name='user-detail'),
    path('users/uploads/<int:pk>/', UserUploads.as_view(), name='user-uploads'),
    path('users/categories/<int:pk>/', UserCategories.as_view(), name='user-categories'),
    path('videos/', VideoViewSet.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailsViewSet.as_view(), name='video-detail'),
    path('category/', CategoryViewSet.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailsViewSet.as_view(), name='category-detail'),
    path('list/', ListViewSet.as_view(), name='list-list'),
    path('list/<int:pk>/', ListDetailsViewSet.as_view(), name='list-detail'),
]
# + staticfiles_urlpatterns()

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

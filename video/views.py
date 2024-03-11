from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from .serializers import VideoSerializer
from .models import Video
from .tasks import create_backup_export
from rest_framework.response import Response


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# @cache_page(CACHE_TTL)

def export_backend_view(request):
    backup_json = create_backup_export()
    return HttpResponse(backup_json)

class VideoViewSet(APIView):
    def get(self, request, format=None):
        """
        Get Request for Get all Video Objects from Videos DB 
        """
        videos = Video.objects.all().order_by('created_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        """
        Post Request for Upload Video Object in Videos DB 
        """
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
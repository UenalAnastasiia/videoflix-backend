from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.views import APIView

import video_list
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


class VideoDetailsViewSet(APIView):
    """
    Video Details Class
    """
    def get(self, request, pk):
        """
        Get Request for Get Video Object by pk from Videos DB 
        """
        try:
            video = Video.objects.filter(id=pk)
            serializer = VideoSerializer(video, many=True)
            return Response(serializer.data)
        except Video.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    
    def get_queryset(self, pk):
        """
        Help Queryset for delete and update video objects
        """
        try:
            video = Video.objects.get(id=pk)
            return video
        except Video.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    
    def delete(self, request, pk, format=None):
        """
        Delete Request for Delete Video Object by pk in Videos DB 
        """
        video = self.get_queryset(pk)
        video.delete()
        video_list.views.deleteListByDeleteVideo(request, pk)
        return Response(status.HTTP_204_NO_CONTENT)
    
    
    def patch(self, request, pk, format=None):
        """
        Patch Request for Update Video Object by pk in Videos DB 
        """
        video_object = self.get_queryset(pk)

        serializer = VideoSerializer(video_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)


class UserUploads(APIView):
    def get(self, request, pk):
        """
        Get Request for Get all User Uploads from Videos DB 
        """
        videos = Video.objects.filter(creator=pk).order_by('created_at')
        print('DATA: ', request)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
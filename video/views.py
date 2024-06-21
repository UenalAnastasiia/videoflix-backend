from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
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
    """
    Exports the video content as a JSON backup in the backend.

    Returns:
        HttpResponse: An HTTP response with the exported JSON content.

    Notes:
        - Uses the `create_backup_export()` function to export the video content.
    """
    backup_json = create_backup_export()
    return HttpResponse(backup_json)


class VideoViewSet(APIView):
    """
    ViewSet for video objects.
    """
    def get(self, request, format=None):
        """
        GET request to retrieve all video objects from the video database.
        """
        videos = Video.objects.all().order_by('created_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        POST request to upload a new video object to the video database.
        """
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class VideoDetailsViewSet(APIView):
    """
    Class for detailed views of video objects.
    """
    def get(self, request, pk):
        """
        GET request to retrieve a specific video object from the database using the primary key.
        """
        try:
            video = Video.objects.filter(id=pk)
            serializer = VideoSerializer(video, many=True)
            return Response(serializer.data)
        except Video.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get_queryset(self, pk):
        """
        Helper Query Set for deleting and updating video objects.
        """
        try:
            video = Video.objects.get(id=pk)
            return video
        except Video.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete(self, request, pk, format=None):
        """
        DELETE request to delete a specific video object from the database using the primary keys.
        """
        video = self.get_queryset(pk)
        video.delete()
        video_list.views.deleteListByDeleteVideo(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, format=None):
        """
        PATCH request to update a specific video object using the primary keys in the database.
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
        GET request to retrieve all videos uploaded by the user from the videos database.
        """
        videos = Video.objects.filter(creator=pk).order_by('created_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

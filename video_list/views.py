from rest_framework import status
from rest_framework.views import APIView
from .serializers import ListSerializer
from .models import List
from rest_framework.response import Response


class ListViewSet(APIView):    
    def post(self, request, format=None):
        """
        POST request to upload a list object to the video list database.
        """
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetailsViewSet(APIView):
    """
    Class for detailed views of list objects.
    """
    def get(self, request, pk):
        """
        GET request to retrieve list objects from the video database based on the user ID.
        """
        try:
            video = List.objects.filter(creator=pk)
            serializer = ListSerializer(video, many=True)
            return Response(serializer.data)
        except List.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)


class ListOptionsViewSet(APIView):
    def get_queryset(self, pk):
        """
        Helper Query Set for deleting and updating list objects.
        """
        try:
            return List.objects.get(id=pk)
        except List.DoesNotExist:
            raise Exception("List object not found")

    def delete(self, request, pk, format=None):
        """
        DELETE request to delete a list object using the primary keys in the video list database.
        """
        try:
            list = self.get_queryset(pk)
            list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if str(e) == "List object not found":
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def deleteListByDeleteVideo(request, pk):
    """
    Function for deleting lists based on the video ID.
    """
    list = List.objects.filter(list=pk)
    list.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

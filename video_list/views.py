from rest_framework import status
from rest_framework.views import APIView
from .serializers import ListSerializer
from .models import List
from rest_framework.response import Response


class ListViewSet(APIView):    
    def post(self, request, format=None):
        """
        Post Request for Upload List Object in Video List DB 
        """
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ListDetailsViewSet(APIView):
    """
    List Details Class
    """
    def get(self, request, pk):
        """
        Get Request for Get List Object by User ID from Videos DB 
        """
        try:
            video = List.objects.filter(creator=pk)
            serializer = ListSerializer(video, many=True)
            return Response(serializer.data)
        except List.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    
    def get_queryset(self, pk):
        """
        Help Queryset for delete and update List objects
        """
        try:
            list = List.objects.get(id=pk)
            print('ID ', pk)
            return list
        except List.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    
    def delete(self, request, pk, format=None):
        """
        Delete Request for Delete List Object by pk in Video List DB 
        """
        list = self.get_queryset(pk)
        list.delete()
        return Response(status.HTTP_204_NO_CONTENT)


def deleteListByDeleteVideo(request, pk):
    list = List.objects.filter(list=pk)
    list.delete()
    return Response(status.HTTP_204_NO_CONTENT)
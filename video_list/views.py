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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            raise Response(status=status.HTTP_404_NOT_FOUND)
    
    
    def get_queryset(self, pk):
        """
        Help Queryset for delete and update List objects
        """
        try:
            list = List.objects.get(id=pk)
        except List.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        
    
    def delete(self, request, pk, format=None):
        """
        Delete Request for Delete List Object by pk in Video List DB 
        """
        try:
            list = self.get_queryset(pk)
            if list:
                list.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def deleteListByDeleteVideo(request, pk):
    list = List.objects.filter(list=pk)
    list.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CategorySerializer
from .models import Category


class CategoryViewSet(APIView):    
    def get(self, request, format=None):
        """
        Get Request for Get all Category Objects from Category DB 
        """
        cat = Category.objects.all()
        serializer = CategorySerializer(cat, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        """
        Post Request for Create Category Object in Category DB 
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class CategoryDetailsViewSet(APIView):
    """
    Category Details Class
    """
    def get(self, request, pk):
        """
        Get Request for Get Category Object by pk from Category DB 
        """
        try:
            category = Category.objects.filter(id=pk)
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    
    def get_queryset(self, pk):
        """
        Help Queryset for update category objects
        """
        try:
            category = Category.objects.get(id=pk)
            return category
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    
    def patch(self, request, pk, format=None):
        """
        Patch Request for Update Category Object by pk in Categories DB 
        """
        category_object = self.get_queryset(pk)

        serializer = CategorySerializer(category_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)

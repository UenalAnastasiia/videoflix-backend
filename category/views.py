from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CategorySerializer
from .models import Category


class CategoryViewSet(APIView):    
    def get(self, request, format=None):
        """
        Get all Category Objects from Category DB 
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create Category Object in Category DB 
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailsViewSet(APIView):
    """
    Category Details Class
    """
    def get_object(self, pk):
        """
        Get Category Object by pk from Category DB 
        """
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        """
        Update Category Object by pk in Categories DB 
        """
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete Category Object by pk in Categories DB 
        """
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCategories(APIView):
    def get(self, request, pk):
        """
        Get all Categories from Category DB created by User
        """
        categories = Category.objects.filter(creator=pk)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

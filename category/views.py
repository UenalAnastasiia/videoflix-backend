from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CategorySerializer
from .models import Category


class CategoryViewSet(APIView):
    """
    API ViewSet for general category operations.
    """
    def get(self, request, format=None):
        """
        Returns all category objects from the category database. 
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Creates a new category object in the category database. 
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailsViewSet(APIView):
    """
    API ViewSet for specific category operations.
    """
    def get_object(self, pk):
        """
        Retrieves a category object from the category database using the primary key (pk). 
        """
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        """
        Returns a specific category object. 
        """
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        """
        Partially updates a specific category object. 
        """
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes a specific category object. 
        """
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCategories(APIView):
    """
    API ViewSet for retrieving categories of a specific user.
    """
    def get(self, request, pk):
        """
        Returns all categories created by a specific user.
        """
        categories = Category.objects.filter(creator=pk)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

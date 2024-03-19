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

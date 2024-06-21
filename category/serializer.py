from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """"
    Serialiser for serialising and deserialising category objects.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'creator', 'content']

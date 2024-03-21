from rest_framework import serializers
from django.contrib.auth.models import User
from .models import List


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class ListSerializer(serializers.ModelSerializer ):
    creator = CreatorSerializer

    class Meta:
        model = List
        fields = '__all__'
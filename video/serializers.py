from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class VideoSerializer(serializers.ModelSerializer ):
    creator = CreatorSerializer

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'creator', 'video_file']
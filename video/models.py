from datetime import date
from django.db import models
from user.models import CustomUser


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    cover_picture = models.FileField(upload_to='covers', blank=True, null=True)
    category = models.CharField(max_length=50, null=True)
    release_year = models.CharField(max_length=20, null=True)
    age = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title

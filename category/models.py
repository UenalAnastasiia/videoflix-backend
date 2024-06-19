from django.db import models
from virtualenv.app_data import read_only
from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=20)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    content = models.BooleanField(null=True)
    status_data = read_only

    def __str__(self):
        return self.name

from django.db import models
from user.models import CustomUser


class List(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    list = models.CharField(max_length=80)

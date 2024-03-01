import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from video.tasks import convert_video_480p
from .models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Save file to filesystem
    """
    print('Video wurde gespreichert')
    if created:
        convert_video_480p(instance.video_file.path)
        


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
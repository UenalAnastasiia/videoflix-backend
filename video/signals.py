import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from video.tasks import convert_video_360p, convert_video_720p, convert_video_1080p
from .models import Video
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Save file to filesystem
    """
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video_360p, instance.video_file.path)
        queue.enqueue(convert_video_720p, instance.video_file.path)
        queue.enqueue(convert_video_1080p, instance.video_file.path)
        

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes files from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            converts = ['', '_360p', '_720p', '_1080p']
            for p in converts:
                filename, extension = os.path.splitext(instance.video_file.path)
                converted_video = filename + p + extension
                if os.path.isfile(converted_video):
                    os.remove(converted_video)
    
    if instance.cover_picture:
        if os.path.isfile(instance.cover_picture.path):
            os.remove(instance.cover_picture.path)
import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from video.tasks import convert_video_360p, convert_video_720p, convert_video__1080p
from .models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Save file to filesystem
    """
    if created:
        convert_video_360p(instance.video_file.path)
        convert_video_720p(instance.video_file.path)
        convert_video__1080p(instance.video_file.path)
        

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    converts = ['_360p', '_720p', '_1080p']
    
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            for p in converts:
                filename, extension = os.path.splitext(instance.video_file.path)
                converted_video = filename + p + extension
                if os.path.isfile(converted_video):
                    os.remove(converted_video)
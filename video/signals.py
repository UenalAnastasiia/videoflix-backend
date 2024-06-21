import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from video.tasks import convert_video_360p, convert_video_720p, convert_video_1080p
from .models import Video
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler to save files to the filesystem when a Video object is saved.

    Args:
        sender (Video): The model class.
        instance (Video): The actual instance being saved.
        created (bool): Boolean flag indicating if the instance was created.
        **kwargs: Additional keyword arguments.

    Notes:
        - Saves the video file in different resolutions (360p, 720p, 1080p) using background jobs.
    """
    if created and instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video_360p, instance.video_file.path)
        queue.enqueue(convert_video_720p, instance.video_file.path)
        queue.enqueue(convert_video_1080p, instance.video_file.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Signal handler to delete files from the filesystem when a Video object is deleted.

    Args:
        sender (Video): The model class.
        instance (Video): The actual instance being deleted.
        **kwargs: Additional keyword arguments.

    Notes:
        - Deletes the original video file and its converted versions (if any) upon deletion of the Video object.
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

import os
import subprocess
from .resources import VideoResource
from datetime import datetime
from django.conf import settings


def convert_video_360p(input):
    """
    Converts a video to 360p resolution with ffmpeg and saves it to the file system.

    Args:
        input (str): The file path to the input video.

    Hints:
        - Uses ffmpeg to convert the video to 360p resolution.
        - Saves the converted file in the same directory with "_360p" as a suffix in the file name.
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_360p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -vf scale=-1:360 -c:v libx264 -crf 18 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)


def convert_video_720p(input):
    """
    Converts a video to 720p resolution with ffmpeg and saves it to the file system.

    Args:
        input (str): The file path to the input video.

    Notes:
        - Uses ffmpeg to convert the video to 720p resolution.
        - Saves the converted file in the same directory with "_720p" as a suffix in the file name.
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_720p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)


def convert_video_1080p(input):
    """
    Converts a video to 1080p resolution with ffmpeg and saves it to the file system.

    Args:
        input (str): The file path to the input video.

    Hints:
        - Uses ffmpeg to convert the video to 1080p resolution.
        - Saves the converted file in the same directory with "_1080p" as a suffix in the file name.
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_1080p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)


def create_backup_export():
    """
    Creates a backup of the video content in JSON format in the "BACKUP_ROOT" directory.

    Returns:
        str: The JSON content of the backup.

    Notes:
        - Uses the Django `VideoResource` to export the video content.
        - Saves the backup as a JSON file in the directory specified in the Django settings under `BACKUP_ROOT`.
    """
    video_resource = VideoResource()
    dataset = video_resource.export()
    backup_json = dataset.json
    created_at = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(settings.BACKUP_ROOT, f"backup_{created_at}.json")
    os.makedirs(settings.BACKUP_ROOT, exist_ok=True)
    with open(path, 'w') as file:
        file.write(backup_json)
    return backup_json

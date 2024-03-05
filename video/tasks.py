import os
import subprocess
from .resources import VideoResource
from datetime import datetime
from django.conf import settings


def convert_video_360p(input):
    """
    Convert Video from Input in 360p with ffmpeg and save it to filesystem
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_360p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -vf scale=-1:360 -c:v libx264 -crf 18 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)
    

def convert_video_720p(input):
    """
    Convert Video from Input in 720p with ffmpeg and save it to filesystem
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_720p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)
    

def convert_video_1080p(input):
    """
    Convert Video from Input in 1080p with ffmpeg and save it to filesystem
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_1080p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)
    

def create_backup_export():
    """
    Create Backup from Video-Content in JSON-Format in directory "backend"
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
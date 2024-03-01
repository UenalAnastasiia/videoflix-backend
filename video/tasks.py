import os
import subprocess


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
    

def convert_video__1080p(input):
    """
    Convert Video from Input in 10800p with ffmpeg and save it to filesystem
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_1080p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)
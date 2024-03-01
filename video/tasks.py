import os
import subprocess


def convert_video_480p(input):
    """
    Convert Video in 480p with ffmpeg and save it to filesystem
    """
    filename, extension = os.path.splitext(input)
    output = filename + '_480p' + extension
    cmd = 'ffmpeg ' + '-i ' + input + ' -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 ' + output
    subprocess.run(cmd, capture_output=True)
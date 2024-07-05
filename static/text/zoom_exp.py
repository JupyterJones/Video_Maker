#!/home/jack/miniconda3/envs/cloned_base/bin/python
import glob
import random
from PIL import Image
from sys import argv
import os
import logging
import subprocess
import uuid
import shutil
import os
import random
import shutil

def prep_homedirectory(source):
    
    home_directory = os.path.expanduser("~") 
    image_directory = os.path.join(home_directory, 'Images')
    print(image_directory)

    # Create or clear the image directory
    if os.path.exists(image_directory):
        shutil.rmtree(image_directory)
        print(f"Cleared contents of image directory: {image_directory}")
    os.makedirs(image_directory, exist_ok=True)
    print(f"Created image directory: {image_directory}")

    # Copy all jpg files from source to image_directory
    for f in os.listdir(source):
        if f.endswith('.jpg'):
            shutil.copy(os.path.join(source, f), image_directory)

    # Get the list of image files in the directory
    image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]
    print(image_files)

    # Shuffle the list of image files
    random.shuffle(image_files)
    print("----------------------------")
    print(image_files)

    # Create a shuffled image directory to store the shuffled images temporarily
    shuffled_directory = os.path.join(home_directory, 'Images', 'shuffled_images')
    os.makedirs(shuffled_directory, exist_ok=True)

    # Copy the shuffled images to the shuffled directory
    for f in image_files:
        shutil.copy(os.path.join(image_directory, f), shuffled_directory)
    return shuffled_directory


def image_dir_to_zoom(selected_directory):
    SIZE = Image.open(random.choice(glob.glob(selected_directory+"/*.jpg"))).size
    
    # Specify the output video file path
    output_video = os.path.join('static', 'output', 'notebook_generated_video.mp4')
    # Frame rate for the output video (adjust as needed)
    frame_rate = 60   # Adjust the frame rate as needed
    # Initialize the FFmpeg command
    ffmpeg_cmd = [
       'ffmpeg',
       '-framerate', str(frame_rate),
       '-i', os.path.join(selected_directory, '%05d.jpg'),  # Modify the format if necessary
       ]
    width = SIZE[0]
    height = SIZE[1]
   

    # Adjust these parameters as needed
    zoom_increment = 0.0005
    zoom_duration = 300  # Increase for a longer zoom duration
    frame_rate = 60  # Increase the frame rate
    ffmpeg_cmd += [
            '-vf', f"scale=8000:-1,zoompan=z='min(zoom+{zoom_increment},1.5)':x='iw/2':y='ih/2-4000':d={zoom_duration}:s={width}x{height},crop={width}:{height}:0:256",
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-r', str(frame_rate),  # Adjust the frame rate here
            '-s', f'{width}x{height}',
            '-y',  # Overwrite output file if it exists
            output_video,
           ]

    # Run the FFmpeg command to generate the video
    subprocess.run(ffmpeg_cmd)
    # mp4 video name generated with uuid
    video_name = str(uuid.uuid4()) + 'notebook_zoomed.mp4'
    shutil.copy('static/assets/generated_video.mp4', os.path.join('static/assets', video_name))
    # Now, render the HTML template and pass the context variables
    output_vid = os.path.join('assets', 'generated_video.mp4')
    print(video_name,":",output_video)
    return output_vid
if __name__=="__main__":
    selected_directory = argv[1]
    source = "/home/jack/Desktop/HDD500/collections/images/an_orc/"
    selected_directory = prep_homedirectory(source)
    image_dir_to_zoom(selected_directory)
    cmd = 'ffmpeg', '-i', 'static/assets/generated_video.mp4', '-vf', 'setpts=0.1*PTS', '-c:a', 'copy', 'static/assets/generated_videoF.mp4'
    subprocess.run(cmd)
    cmd2 ='overlay_pad', 'static/assets/generated_videoF.mp4'
    subprocess.run(cmd2)

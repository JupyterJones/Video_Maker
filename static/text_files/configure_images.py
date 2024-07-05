import shutil
import random
import os

source = '/home/jack/Desktop/HDD500/collections/images/Queen/'
image_directory = '/home/jack/Desktop/FlaskAppArchitect_Flask_App_Creator/static/images/Queen/'

# copy all jpg files from source to image_directory
for f in os.listdir(source):
    if f.endswith('*.jpg'):
        shutil.copy(source + f, image_directory)

# Get the list of image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]
print(image_files)
# Shuffle the list of image files
random.shuffle(image_files)
print("----------------------------")
print(image_files)
# Create a shuffled image directory to store the shuffled images temporarily
shuffled_directory = '/home/jack/Desktop/FlaskAppArchitect_Flask_App_Creator/static/images/shuffled_images'
os.makedirs(shuffled_directory, exist_ok=True)

# Copy the shuffled images to the shuffled directory
for f in image_files:
    shutil.copy(os.path.join(image_directory, f), shuffled_directory)

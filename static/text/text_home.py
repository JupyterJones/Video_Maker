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




source = "/home/jack/Desktop/HDD500/collections/images/an_orc/"
prep_homedirectory(source)



import os
import fnmatch
from mutagen.mp3 import MP3
import random
import subprocess
from flask import Flask, render_template, request, redirect, url_for, Blueprint, send_from_directory
import os
import logging
from logging.handlers import RotatingFileHandler
import uuid
# Configure this files logger
# Configure logging
current_dir = os.getcwd()+'/mp3_sound/mp3sound.log'
#print("Current working directory: {0}".format(current_dir))
# Create a file handler to write log messages to a single file with rotation
file_handler = RotatingFileHandler(current_dir, maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Set the formatter for log messages
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')

file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Initialize the Flask app
mp3_sound_bp = Blueprint("mp3_sound", __name__, template_folder="templates", static_folder="static", static_url_path="assets", url_prefix="/mp3_sound")
# Function to create the all_mp3.list file
def create_mp3_list():
    # The directory to start searching for audio files
    base_directory = "/home/jack/"

    # Pattern to match audio files (case-insensitive)
    audio_pattern = "*.mp3"

    # Initialize an empty list to store the valid MP3 file paths
    mp3_files = []

    # Function to validate if a file is a valid MP3
    def is_valid_mp3(file_path):
        try:
            audiofile = MP3(file_path)
            return True
        except Exception:
            return False

    # Recursively search for audio files and validate them
    for root, dirs, files in os.walk(base_directory):
        for filename in fnmatch.filter(files, audio_pattern):
            audio_path = os.path.join(root, filename)
            if is_valid_mp3(audio_path):
                mp3_files.append(audio_path)

    # Write the list of valid MP3 files to all_mp3.list
    # os.getcwd()+'/mp3_sound/mp3sound.log'
    mp3_list = os.getcwd()+"/mp3_sound/all_mp3.list"
    logger.info("MP3_LIST: {0}".format(mp3_list))
    with open(mp3_list, "w") as file:
        for mp3_file in mp3_files:
            file.write(mp3_file + "\n")

    print(f"Found and validated {len(mp3_files)} MP3 files. Saved to all_mp3.list.")

# Execute the function to create the all_mp3.list file when the app starts
create_mp3_list()

# Path to the file containing the list of MP3 files
mp3_list_file = os.getcwd()+"/mp3_sound/all_mp3.list"
# Number of MP3s to select
num_mp3s_to_select = 100

# Output file name
output_file = "static/flask_random_sounds.mp3"
logger.info("Starting mp3_sound")
logger.debug("Current_Working_Directory: {0}".format(os.getcwd()))
@mp3_sound_bp.route('/', methods=['GET', 'POST'])
def sound_index():
    if request.method == 'POST':
        generate_random_sounds()
        return redirect(url_for('mp3_sound.download_file'))
    return render_template('sound_index.html')

@mp3_sound_bp.route('/download_file')
def download_file():
    static_folder = os.path.abspath(os.path.join(os.getcwd(), 'mp3_sound', 'static'))
    output_file = os.path.join(static_folder, "output.mp3")
    logger.info("download_file_Output file: {0}".format(output_file))
    return render_template('download_file.html', output_file=output_file)

def generate_random_sounds():
    # Read the list of MP3 files
    with open(mp3_list_file, "r") as file:
        mp3_files = file.readlines()

    # Remove any trailing whitespace and ensure absolute paths
    mp3_files = [os.path.abspath(file.strip()) for file in mp3_files]

    # Select random MP3 files
    selected_mp3s = random.sample(mp3_files, num_mp3s_to_select)

    # Initialize a list to store the clips
    clips = []

    # Extract one-second clips from each selected MP3 file
    for mp3_file in selected_mp3s:
        # Generate a random start time (in seconds)
        start_time = random.uniform(0, 1)  # Adjust to your desired range
        output_clip = f"clip_{len(clips) + 1}.mp3"

        try:
            # Use ffmpeg to extract the one-second clip
            subprocess.run(["ffmpeg", "-i", mp3_file, "-ss", str(start_time), "-t", "1", "-y", output_clip])
            clips.append(output_clip)
        except FileNotFoundError as e:
            print(f"File not found error: {str(e)}. Skipping...")

    # Concatenate the one-second clips
    concatenation_command = ["ffmpeg"]
    concatenation_command.extend(["-i", f"concat:{'|'.join(clips)}"])
    concatenation_command.extend(["-c", "copy", "-y", output_file])
    logger.info("Concatenation command: {0}".format(concatenation_command))
    logger.info("Clips: {0}".format(output_file))

    subprocess.run(concatenation_command)

    # Clean up temporary one-second clips
    mp3_filename = os.getcwd()+'/mp3_sound/static/flask_random_sounds.ogg'
    logger.info("MP3_FILENAME: {0}".format(mp3_filename))
    #for clip in clips:
    #    if os.path.exists(clip):
    #        os.remove(clip)
    subprocess.run(["ffmpeg", "-i", "static/flask_random_sounds.mp3", "-c:a", "libvorbis","-y" ,mp3_filename])



# Route for joining two MP3 files with volume adjustment
@mp3_sound_bp.route("/join_sound", methods=["GET", "POST"])
def join_sound():
    if request.method == "POST":
        mp3_file1 = request.form["mp3_file1"]
        mp3_file2 = request.form["mp3_file2"]
        volume1 = float(request.form["volume1"])
        volume2 = float(request.form["volume2"])
        mp3_dir = os.path.abspath(os.path.join(os.getcwd(), 'mp3_sound', 'static'))  # Directory where MP3 files are stored
        input_file1 = os.path.join(mp3_dir, mp3_file1)  # Full path to input file 1
        input_file2 = os.path.join(mp3_dir, mp3_file2)  # Full path to input file 2
        output_file = os.path.join(mp3_dir, "output.mp3")  # Full path to output file
        
        # Log the inputs for debugging
        logger.info("Received request to merge MP3 files.")
        logger.info("MP3_FILE1: {0}".format(input_file1))
        logger.info("MP3_FILE2: {0}".format(input_file2))
        logger.info("VOLUME1: {0}".format(volume1))
        logger.info("VOLUME2: {0}".format(volume2))
        logger.info("OUTPUT_FILE: {0}".format(output_file))
        
        try:
            # Call the merge_mp3_files function to merge the MP3 files
            logger.info("Calling merge_mp3_files function.")
            logger.info("MP3_FILE1: {0}".format(input_file1))
            logger.info("MP3_FILE2: {0}".format(input_file2)) 
            logger.info("VOLUME1: {0}".format(volume1)) 
            logger.info("VOLUME2: {0}".format(volume2))
            logger.info("OUTPUT_FILE: {0}".format(output_file))
            
            merge_mp3_files(input_file1, input_file2, volume1, volume2, output_file)
            
            # Provide a link to download the merged MP3 file
            return f"Joined MP3 file created: <a href='{output_file}'>Download</a>"
        except Exception as e:
            # Log any exceptions that occur during the merge
            logger.error("Error while merging MP3 files: {0}".format(str(e)))
            return "Error occurred while merging MP3 files."
    
    # Send output file to the template
    static_folder = os.path.abspath(os.path.join(os.getcwd(), 'mp3_sound', 'static'))
    output_file = os.path.join(static_folder, "output.mp3")

    return render_template("join_sound.html", output_file=output_file)


# Route to serve the merged MP3 file
@mp3_sound_bp.route("/download/<filename>")
def download(filename):
    static_folder = os.path.abspath(os.path.join(os.getcwd(), 'mp3_sound', 'static'))
    logger.info("Download_Filename: {0}".format(filename))
    return send_from_directory(static_folder, filename)

def merge_mp3_files(input_file1, input_file2, volume1, volume2, output_file):
    try:
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-i", input_file1,
            "-i", input_file2,
            "-filter_complex",
            f"[0:a]volume={volume1}[a];[1:a]volume={volume2}[b];[a][b]amix=inputs=2:duration=first[aout]",
            "-map", "[aout]",
            "-y", output_file
        ]

        logger.info("Executing FFmpeg command:")
        logger.info(" ".join(cmd))

        # Execute the ffmpeg command
        subprocess.run(cmd, check=True)

        # Log a success message
        logger.info("MP3 files merged successfully.")
    except subprocess.CalledProcessError as e:
        # Log any errors that occur during the ffmpeg process
        logger.error("Error while merging MP3 files with ffmpeg: {0}".format(str(e)))
        raise  # Re-raise the exception to handle it in the calling function
    except Exception as e:
        # Log any other exceptions
        logger.error("An error occurred: {0}".format(str(e)))
        raise
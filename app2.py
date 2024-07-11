#!/home/jack/Desktop/Video_Maker/venv/bin/python
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory, send_file, flash, session, jsonify
import os
import datetime
import inspect
from PIL import Image, ImageDraw, ImageFont
import subprocess
import secrets
import sys
import random
import glob
import sqlite3
from icecream import ic
# Generate a secret key for the Flask application
secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = 'your_generated_secret_key_here'
# Define the directory where text files will be stored
TEXT_FILES_DIR = "static/text_files"
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)
# Log to file function
def logit(message):
    try:
        # Get the current timestamp
        timestr = datetime.datetime.now().strftime('%A_%b-%d-%Y_%H-%M-%S')

        # Get the caller's frame information
        caller_frame = inspect.stack()[1]
        filename = caller_frame.filename
        lineno = caller_frame.lineno

        # Convert message to string if it's a list
        if isinstance(message, list):
            message_str = ' '.join(map(str, message))
        else:
            message_str = str(message)

        # Construct the log message with filename and line number
        log_message = f"{timestr} - File: {filename}, Line: {lineno}: {message_str}\n"

        # Open the log file in append mode
        with open("log.txt", "a") as file:
            # Get the current position in the file
            file.seek(0, 2)
            pos = file.tell()

            # Write the log message to the file
            file.write(log_message)

            # Print the log message to the console
            print(log_message)

            # Return the position as the ID
            return pos
    except Exception as e:
        message_str = str(message)
        # If an exception occurs during logit, print an error message
        print(f"Error occurred while creating log: {e}")
logit("Server started")
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_terms')
        results = []
        cnt = 0
        search_terms = search_term.split(",")
        
        with open("static/text/conversations.txt","r") as data:
            Lines = data.read()
            lines = Lines.split("CHAT_DIALOGUE")
            for line in lines:
                for search_term in search_terms:
                    if search_term in line:
                        cnt += 1
                        print(f'line: {cnt}\n{line}')
                        print(f'--------------- {cnt} -----------------')
                        results.append(line) 
     
        return render_template('search.html', results=results)
    return render_template('search.html')

def save_text_to_file(filename, text):
    filepath = os.path.join(TEXT_FILES_DIR, filename)
    with open(filepath, "w") as file:
        file.write(text)
    log_message = f"Text saved to file: {filename}"
    logit(log_message)

# Function to read text from a file
def read_text_from_file(filename):
    filepath = os.path.join(TEXT_FILES_DIR, filename)
    with open(filepath, "r") as file:
        text = file.read()
    log_message = f"Text read from file: {filename}"
    logit(log_message)
    return text

# Function to log messages
def logit(message):
    print(f"[LOG] {message}")

def sort_files_by_date(directory):
    DATED = []
    try:
        # Get list of files
        files = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
        logit(f"Files found: {files}")

        # Sort files by modification date
        files.sort(key=lambda x: os.path.getmtime(x))
        logit(f"Files sorted by date: {files}")

        # Print sorted files with modification dates
        for file in files:
            mod_time = os.path.getmtime(file)
            formatted_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{file} - Last modified: {formatted_time}")
            DATED.append(f"{file}")
            logit(f"File: {file} - Last modified: {formatted_time}")
        logit(f"List of sorted files: {DATED}")    
        return DATED

    except Exception as e:
        logit(f"An error occurred: {e}")


@app.route("/editor", methods=["GET", "POST"])
def editor():
    if request.method == "POST":
        filename = request.form["filename"]
        text = request.form["text"]
        save_text_to_file(filename, text)
        return redirect(url_for("editor"))
    else:
        #files = os.listdir(TEXT_FILES_DIR)
        #files = files.sort(key=lambda x: os.path.getmtime(x))
        files = sorted(
                [file for file in os.listdir(TEXT_FILES_DIR) if os.path.isfile(os.path.join(TEXT_FILES_DIR, file))],
                key=lambda x: os.path.getmtime(os.path.join(TEXT_FILES_DIR, x)),reverse=True)

        logit(files)
        #files = sort_files_by_date(TEXT_FILES_DIR)
        return render_template("editor1.html", files=files)

@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit(filename):
    if request.method == "POST":
        text = request.form["text"]
        logit(f"Text edited in file: {filename}")
        logit(text)
        save_text_to_file(filename, text)
        return redirect(url_for("editor"))
    else:
        text = read_text_from_file(filename)
        return render_template("edit1.html", filename=filename, text=text)


@app.route("/delete/<filename>")
def delete(filename):
    filepath = os.path.join(TEXT_FILES_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        log_message = f"File deleted: {filename}"
        logit(log_message)
    return redirect(url_for("editor"))

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(TEXT_FILES_DIR, filename, as_attachment=True)

@app.route('/create_text', methods=['GET', 'POST'])
def create_text():
    if request.method == 'POST':
        text = request.form['text']
        image = Image.new('RGB', (512, 512), color='beige')
        draw = ImageDraw.Draw(image)
        # use 26 as the font size
        font=ImageFont.truetype("/home/jack/fonts/Almendra-Bold.ttf", 26)
        #font = ImageFont.load_default()  # You can use a different font if needed
        lines = text.split('\n')[:5]  # Get the first 5 lines

        y = 10
        for line in lines:
            draw.text((10, y), line, fill='black', font=font)
            y += 20  # Move down for the next line

        output_path = os.path.join(app.root_path, 'static', 'assets', '512x512_text.jpg')
        image.save(output_path)
        return render_template('create_text.html', text=text, image=output_path)

    return render_template('create_text.html')  # Create this template as described below

@app.route('/utilities', methods=['GET', 'POST'])
def utilities():
    if request.method == 'POST':
        filename = request.form['filename']
        filepath = 'static/text_files'
        # Ensure the filepath and filename are safe and valid
        script_path = os.path.join(filepath, filename)
        logit(f"SCRIPT: ,{script_path}")
        if not os.path.exists(script_path):
            flash('File not found. Please check the filename and path.', 'error')
            return redirect(url_for('utilities'))
        try:
            result = subprocess.run(['/home/jack/miniconda3/envs/cloned_base/bin/python', script_path], capture_output=True, text=True, check=True)
            output = result.stdout
            logit(f"Script {script_path} executed successfully.")
        except subprocess.CalledProcessError as e:
            output = e.stderr
            logit(f"An error occurred while executing the script {script_path}: {e}")
        return render_template('utilities.html', result=output)

    return render_template('utilities.html')
@app.route('/bash', methods=['GET', 'POST'])
def bash():
    if request.method == 'POST':
        filename = request.form['filename']
        arg = request.form['arg']
        filepath = 'static/text_files'
        # Ensure the filepath and filename are safe and valid
        script_path = os.path.join(filepath, filename)
        if not os.path.exists(script_path):
            flash('File not found. Please check the filename and path.', 'error')
            return redirect(url_for('bash'))

        try:
            # Run the Python script or any command using subprocess
            
            cmd=['/bin/bash', script_path,arg]
            logit(cmd)
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
            logit(f"Script {script_path} executed successfully.")
        except subprocess.CalledProcessError as e:
            output = e.stderr
            logit(f"An error occurred while executing the script {script_path}: {e}")

        return render_template('bash.html', result=output)

    return render_template('bash.html')
@app.route('/terminal_index')
def terminal_index():
    return render_template('terminal_index.html')
@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.form.get('command')
    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    return jsonify({'output': output})

@app.route('/index_bash')
def index_bash():
    video = findvideos()
    return render_template('run_bash.html', video=video)

def findvideos():
    videoroot_directory = "static"
    MP4 = []
    for dirpath, dirnames, filenames in os.walk(videoroot_directory):
        for filename in filenames:
            if filename.endswith(".mp4"): #and "Final" in filename:
                MP4.append(os.path.join(dirpath, filename))
    if MP4:
        last_video = session.get("last_video")
        new_video = random.choice([video for video in MP4 if video != last_video])
        session["last_video"] = new_video
        return new_video
    else:
        return None

@app.route('/run_bash', methods=['POST', 'GET'])
def run_bash():
    bash_command = request.form.get('bash_command')
    
    try:
        result = subprocess.check_output(bash_command, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output
    video = findvideos()
    return render_template('run_bash.html', result=result, video=video)

def get_files():
    files = [file for file in os.listdir(TEXT_FILES_DIR) if os.path.isfile(os.path.join(TEXT_FILES_DIR, file))]
    return files


@app.route('/edittext', methods=['GET', 'POST'])
def edittext():
    if request.method == 'POST':
        text = request.form['text']
        # Handle saving the text or processing it as needed
        return render_template('edittext.html', text=text, files=get_files())
    return render_template('edittext.html', files=get_files())
def read_functions():
    with open('static/text_files/completion.txt', 'r') as file:
        code = file.read()
        #code = code.decode('utf-8')
        verses = code.split('\n\n') # Splitting text into verses based on empty lines
        logit("File successfully read and verses extracted.")
    return verses

functions = read_functions()

def generate_suggestions(code):
    logit("Generating suggestions...")
    # Retrieve the last line from the code
    lines = code.split('\n')
    last_line = lines[-1]

    # Split the last line into words and get the last four words
    words = last_line.split()
    last_four_words = ' '.join(words[-2:])
    logit(f"Last four words: {last_four_words}")

    # Search for a matching snippet based on the last four words
    matching_snippets = []
    for i, snippet in enumerate(functions, start=1):
        if last_four_words in snippet:
            # Format the snippet with line numbers and preserve whitespace
            formatted_snippet = f"{i}:: <br/><pre>{snippet.strip()}</pre>"
            matching_snippets.append(formatted_snippet)

    logit(f"Matching snippets: {matching_snippets}")

    return matching_snippets
@app.route('/index_code')
def index_code():
    return render_template('index_code.html')

@app.route('/save', methods=['POST'])
def save():
    code = request.form['code']
    logit(f"Received code: {code}")
    suggestions = generate_suggestions(code)
    logit(f"Generated suggestions: {suggestions}")
    return {'suggestions': suggestions}
@app.route('/save_code', methods=['POST'])
def save_code():
    # Extract the code from the request body
    code = request.data.decode('utf-8')
    if code:
        # Append the code to the new_app.py file
        with open('new_app.py', 'a') as file:
            file.write(code + '\n')
        return 'Code saved successfully', 200
    else:
        return 'No code provided in the request', 400


@app.route('/index_base', methods=['POST', 'GET'])
def index_base():
    return render_template('index_base.html')

@app.route('/index_text_db', methods=['POST', 'GET'])
def index_text_db():
    return render_template('index_text_db.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('app_index.html')

''' database schema
CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        content BLOB NOT NULL,
        text_content TEXT NOT NULL,
        hash_value TEXT NOT NULL,
        format TEXT NOT NULL
    )

'''
@app.route('/search_db', methods=['GET', 'POST'])
def search_db():
    data = []
    if request.method == 'POST':
        if 'text' in request.form:
            search_term = request.form['text']
            conn = sqlite3.connect('static/database/video_text.db')
            cursor = conn.cursor()
            cnt = 0

            # Define the search terms
            search_terms = search_term.split(" ")  # Split the input string by comma to get individual search terms

            # Construct the WHERE clause for the SQL query to filter rows based on all search terms
            where_conditions = []
            for term in search_terms:
                where_conditions.append(f"text_content LIKE '%{term.strip()}%'")
            where_clause = " AND ".join(where_conditions)

            # Execute the SELECT query with the constructed WHERE clause
            query = f"SELECT ROWID, * FROM files WHERE {where_clause} ORDER BY ROWID DESC LIMIT 2"
            rows = cursor.execute(query)

            # Iterate over the resulting rows and append to data list
            for row in rows:
                cnt += 1
                data.append(f'{row[1]} {row[2]} \n\n {row[4]} {cnt}')

            conn.close()
    
    return render_template('search_db.html', data=data)


@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    # Adjust the path to your image directory
    images_path = os.path.join(app.static_folder, 'app_images', '*.jpg')
    images = glob.glob(images_path)
    # Extract just the filenames for URL generation
    images = [os.path.basename(image) for image in images]
    return render_template('gallery.html', images=images)

@app.route('/video_gallery', methods=['POST', 'GET'])
def video_gallery():
    ic("Video gallery accessed")
    logit("Video gallery accessed")
    # Adjust the path to your image directory
    #/home/jack/Desktop/Video_Maker/static/videos/
    videos_path = os.path.join(app.static_folder, 'videos', '*.mp4')
    videos = glob.glob(videos_path)
    # Extract just the filenames for URL generation
    videos = [os.path.basename(video) for video in videos]
    logit(f"Videos: {videos}")
    ic(videos)
    return render_template('video_gallery.html', videos=videos)


if __name__ == '__main__':
    # change directory to /home/jack/Desktop/Video_Maker/
    os.chdir('/home/jack/Desktop/Video_Maker/')
    app.run(debug=True, host='0.0.0.0', port=5200)

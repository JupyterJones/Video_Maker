#!/home/jack/miniconda3/envs/cloned_base/bin/python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
import datetime
import inspect
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)

# Define the directory where text files will be stored
TEXT_FILES_DIR = "static/text_files"
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)
# Logging function
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
        # If an exception occurs during logging, print an error message
        print(f"Error occurred while logging: {e}")
logit("Server started")
@app.route('/', methods=['GET', 'POST'])
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

@app.route("/editor", methods=["GET", "POST"])
def editor():
    if request.method == "POST":
        filename = request.form["filename"]
        text = request.form["text"]
        save_text_to_file(filename, text)
        return redirect(url_for("editor"))
    else:
        try:
            files = [os.path.join(TEXT_FILES_DIR, file) for file in os.listdir(TEXT_FILES_DIR) if os.path.isfile(os.path.join(TEXT_FILES_DIR, file))]
            files = glob.glob(TEXT_FILES_DIR + "/*.*")
            files.sort(key=lambda x: os.path.getmtime(x))
            logit("List of files retrieved for editor view")
            
            # Preparing file info to pass to the template
            file_infos = []
            for file in files:
                mod_time = os.path.getmtime(file)
                formatted_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                file_infos.append({"name": os.path.basename(file), "mod_time": formatted_time})
            
            return render_template("editor1.html", files=file_infos)
        except Exception as e:
            logit(f"An error occurred while listing files: {e}")
            return render_template("editor1.html", files=[])

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5200)

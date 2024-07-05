from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)

# Define the directory where text files will be stored
TEXT_FILES_DIR = "static/text_files"
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)

# Function to save text to a file
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
        files = os.listdir(TEXT_FILES_DIR)
        logit("List of files retrieved for editor view")
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

if __name__ == "__main__":
    app.run(debug=True)

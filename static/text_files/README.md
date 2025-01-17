
$ git clone https://github.com/JupyterJones/Video_Maker.git
$ cd Video_Maker 

# Set up a virtual environment:

## If you do not have virtualenv
## Install venv
!pip install virtualenv

## Specify the path where you want to create the virtual environment. You may call your virtual environment what you wish. I will use flask_venv

# Create a virtual environment
python -m venv flask_venv

# Activate the virtual environment 
source flask_venv/bin/activate

To ensure that your project runs smoothly with Flask, MoviePy, voice creation, and OpenCV, you'll need to list the required packages in your requirements.txt file. Below is a requirements.txt file that includes the necessary packages for these functionalities:

plaintext
----- in the requirements.txt ------

flask==2.1.1
moviepy==1.0.3
gtts==2.2.3
opencv-python==4.8.0.74
numpy==1.22.3
scipy==1.8.0
werkzeug==2.2.3
waitress==2.1.2
pydub==0.25.1
requests==2.27.1
setuptools==65.5.1
urllib3==1.26.9


Explanation of Packages:
flask==2.1.1: Flask framework for creating web applications.
moviepy==1.0.3: MoviePy library for video editing.
gtts==2.2.3: Google Text-to-Speech library for creating voice files.
opencv-python==4.8.0.74: OpenCV library for computer vision tasks.
numpy==1.22.3: NumPy library for numerical computations (required by MoviePy and OpenCV).
scipy==1.8.0: SciPy library for scientific computing (used by MoviePy).
werkzeug==2.2.3: WSGI utility library for Flask.
waitress==2.1.2: WSGI server for production deployment of Flask applications.
pydub==0.25.1: PyDub library for audio manipulation.
requests==2.27.1: Requests library for making HTTP requests.
setuptools==65.5.1: Setuptools for package management.
urllib3==1.26.9: HTTP library with thread-safe 

connection pooling.
Usage:

Create a requirements.txt file in your project directory.
Copy and paste the above content into the requirements.txt file.
Install the packages by running the following command in your terminal:

pip install -r requirements.txt

This will install all the necessary packages specified in the requirements.txt file, ensuring your environment is set up correctly for Flask, MoviePy, voice creation, and OpenCV functionalities.

# Now, you can install packages within the virtual environment
!pip install package_name

pip install -r requirements.txt


# Deactivate the virtual environment:
deactivate

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, this is your Flask app running on the LAN!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

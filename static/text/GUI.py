#!/home/jack/Desktop/FlaskAppArchitect_Flask_App_Creator/env/bin/python
# from flask import Flask  
from flask import render_template, session, Flask
from flaskwebgui import FlaskUI # import FlaskUI
import os 
import random
app = Flask(__name__)


@app.route("/")
def hello():  
    return render_template('about.html')

@app.route("/home", methods=['GET'])
def home(): 
    return render_template('HTML5_Canvas_Cheat_Sheet.html')

@app.route("/about", methods=['GET'])
def about():     
    video=findvideos()
    return render_template('about.html', video=video)
@app.route("/html_base", methods=['GET'])
def html_base(): 
    return render_template('html_base.html')
def findvideos():
    videoroot_directory = "static"
    MP4 = []
    for dirpath, dirnames, filenames in os.walk(videoroot_directory):
        for filename in filenames:
            if filename.endswith(".mp4") and "Final" in filename:
                MP4.append(os.path.join(dirpath, filename))
    if MP4:
        last_video = session.get("last_video")
        new_video = random.choice([video for video in MP4 if video != last_video])
        session["last_video"] = new_video
        return new_video
    else:
        return None

if __name__ == "__main__":
    # If you are debugging you can do that in the browser:
    # If you want to view the flaskwebgui window:
    FlaskUI(app=app, server="flask").run()
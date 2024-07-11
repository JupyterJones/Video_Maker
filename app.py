#!/home/jack/Desktop/Video_Maker/venv/bin/python
import subprocess
import os

if __name__ == '__main__':
    # change directory to /home/jack/Desktop/Video_Maker/
    os.chdir('/home/jack/Desktop/Video_Maker/')
    #subprocess run ' /home/jack/Desktop/Video_Maker/venv/bin/python app2.py'
    cmd = ' /home/jack/Desktop/Video_Maker/venv/bin/python app2.py'
    subprocess.run(cmd, shell=True)
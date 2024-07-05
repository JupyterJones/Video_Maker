import glob
import random

files = random.sample(glob.glob('static/text_files/*.py'),7)
for file in files:
    print(file)
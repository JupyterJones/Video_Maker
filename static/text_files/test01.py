import os 
import glob
import random
cnt=0
files = random.sample(glob.glob('static/text_files/*.py'),5)
for file in files:
   cnt=cnt+1
   print(cnt,file)
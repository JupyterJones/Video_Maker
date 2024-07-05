import os

def search_text(filename,search_term):
     datas = open(filename).read()
     # print(datas)
     datas = datas.replace(search_term,'---index---\n'+search_term)
     cnt=0
     data = datas.split('---index---')
     for line in data:
         if search_term in line:
             cnt=cnt+1
             print(line)
             print('---------',cnt,'--------')
if __name__ == '__main__':
     #search_term= input('Enter Search Term:')
     search_term = 'uploads'
     filename='static/text_files/appbp.txt'
     search_text(filename,search_term)
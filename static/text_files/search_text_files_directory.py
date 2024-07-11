import glob
RESULTS=[]
def search_txt(phrase,filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        results = []
        for i, line in enumerate(lines):
            if phrase in line:
                start = max(0, i - 5)
                end = min(len(lines), i + 6)
                context = lines[start:end]
                for j, context_line in enumerate(context):
                    if phrase in context_line:
                        phrase = phrase.strip()
                        results.append(f'Line {start+j}: {context_line}')
                    else:
                        phrase = phrase.strip()
                        results.append(f'Line {start+j}: {context_line}')
        return results
def search_dir(phrase):
    files = glob.glob('static/text_files/*.*')
    for file in files:
        datas = open(file, 'r').readlines()
        for data in datas:
            if phrase in data:
                RESULTS.append([file,data])
    return RESULTS 
       
if __name__ =='__main__': 
    phrase = 'mosquito'
    Datas = search_dir(phrase)
    for data in Datas:
        print('------------')
        print(data)
    '''
    files = glob.glob('static/text_files/*.*')
    for filename in files:
        results = search_txt(phrase,filename)
        for result in results:
            print('-------------\n')
            print(result)  
    '''
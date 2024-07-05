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
if __name__ =='__main__': 
    phrase = 'management'
    filename = 'static/text_files/AI_will_have_a_thinning_effect.txt'
    results = search_txt(phrase,filename)
    for result in results:
        print(result)  
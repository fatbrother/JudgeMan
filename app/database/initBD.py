import os
from pathlib import Path
import json

base = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute())

problemSets = []
with open(base + '\\problemSetId.txt') as f:
    for line in f:
        id = line.split('  ')[0][1:]
        title = line.split('  ')[1].strip()
        problemSets.append({'id': int(id), 'title': title, 'problemId': []})

for problemSet in problemSets:
    url = base + '\\' + problemSet['title'] + '\\' + 'Description.txt'
    with open(url) as f:
        for line in f:
            problemSet['problemId'].append(int(line.split('.')[0]))

for problemSet in problemSets:
    problemSet['problemId'].sort()


with open('problemSets.json', 'w') as f:
    f.write(json.dumps(problemSets, indent=4))

problems = []
keyWords = ['input format', 'output format',
            'sample input', 'sample output', 'hint',
            '範例輸入', '範例輸出', '提示',
            '輸入格式', '輸出格式']
for problemSet in problemSets:
    url = base + '\\' + problemSet['title'] + '\\' + 'Description.txt'
    with open(url, encoding='utf-8') as f:
        for line in f:
            problems.append(
                {'id': int(line.split('.')[0]), 'title': line.split('.')[1].strip()})
            
            title = line.strip()
            if title[-1] in '.?!':
                title = title[:-1]
            subUrl = base + '\\' + problemSet['title'] + '\\' + title

            with open(subUrl + '\\' + 'Description.txt', encoding='UTF-8') as f:
                lines = f.readlines()
                index = 0
                problems[-1].update({'description': '', 'input_format': '', 'output_format': '',
                                     'sample_input': [], 'sample_output': [], 'hint': '', 'test_case_number': 0, 'AC': 0, 'WA': 0})

                while index < len(lines):
                    if '題目描述' in lines[index] or 'description' in lines[index].lower():
                        index += 1
                        while index < len(lines) and not any(keyWord in lines[index].lower() for keyWord in keyWords):
                            if lines[index][0].isalpha():
                                problems[-1]['description'] += ' '
                            problems[-1]['description'] += lines[index].strip()
                            index += 1
                    elif '輸入格式' in lines[index] or 'input format' in lines[index].lower():
                        index += 1
                        while index < len(lines) and not any(keyWord in lines[index].lower() for keyWord in keyWords):
                            if lines[index][0].isalpha():
                                problems[-1]['input_format'] += ' '
                            problems[-1]['input_format'] += lines[index].strip()
                            index += 1
                    elif '輸出格式' in lines[index] or 'output format' in lines[index].lower():
                        index += 1
                        while index < len(lines) and not any(keyWord in lines[index].lower() for keyWord in keyWords):
                            if lines[index][0].isalpha():
                                problems[-1]['output_format'] += ' '
                            problems[-1]['output_format'] += lines[index].strip()
                            index += 1
                    elif '範例輸入' in lines[index] or 'sample input' in lines[index].lower():
                        index += 1
                        problems[-1]['sample_input'].append('')
                        while index < len(lines) and not any(keyWord in lines[index].lower() for keyWord in keyWords):
                            problems[-1]['sample_input'][-1] += lines[index]
                            index += 1
                    elif '範例輸出' in lines[index] or 'sample output' in lines[index].lower():
                        index += 1
                        problems[-1]['sample_output'].append('')
                        while index < len(lines) and not any(keyWord in lines[index].lower() for keyWord in keyWords):
                            problems[-1]['sample_output'][-1] += lines[index]
                            index += 1
                    elif '提示' in lines[index] or 'hint' in lines[index].lower():
                        index += 1
                        while index < len(lines) and not any(keyWord in lines[index].lower() for keyWord in keyWords):
                            problems[-1]['hint'] += lines[index]
                            index += 1
                    else:
                        index += 1

            # count file number in subUrl + 'testCases'
            if os.path.exists(subUrl + '\\' + 'testCases'):
                problems[-1]['test_case_number'] = len(os.listdir(subUrl + '\\' + 'testCases')) // 2


problems.sort(key=lambda x: x['id'])

with open('problems.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(problems, indent=4, ensure_ascii=False))
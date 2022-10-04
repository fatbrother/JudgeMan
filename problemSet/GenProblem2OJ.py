from pathlib import Path
from json import load, dump
from shutil import copy

output_dir = Path('..', 'output_dir')
totalScore = 100  # per Problem

'''Example Problem
	{
        "id": 12,
        "title": "Up and Down",
        "description": " Write a program to read a positive integer n, then print a sequence of 2n−1 integers from 1 to n, and then from n−1 to 1.",
        "inputFormat": " There is one line in the input. The first line has the integer n.",
        "outputFormat": " There are 2n−1 lines in the output, according to the description.",
        "sampleInput": [
            "5\n"
        ],
        "sampleOutput": [
            "1\n2\n3\n4\n5\n4\n3\n2\n1\n"
        ],
        "hint": "",
        "AC": 1301,
        "WA": 213
    },
'''

global_problem_dict = {}

# load problem json
rawProblems = load(Path('..', 'problems.json').open(encoding='utf8'))
problems = []
for problem in rawProblems:
    for key in ["description", "inputFormat", "outputFormat", "hint"]:
        problem[key] = problem[key].replace('\n', '<br />')

    problem['samples'] = []
    for i in range(len(problem['sampleInput'])):
        problem['samples'].append({
            'input': problem['sampleInput'][i],
            'output': problem['sampleOutput'][i]
        })
    global_problem_dict[f"{problem['id']}. {problem['title']}"] = problem

tag_list = [x for x in Path().iterdir() if x.is_dir()]
for tag in tag_list:  # tag: Path()
    if str(tag) == 'Trash':
        continue
    for problem_path in Path(tag).iterdir():
        problem_path = problem_path.parts[-1]  # problem_path: str
        problem_data = global_problem_dict.get(problem_path)
        if not problem_data:
            continue
        output_work_dir = Path(output_dir, str(problem_data['id']))
        output_work_dir.mkdir(parents=True)

        # Generate test cases
        (testCaseFolder := Path(output_work_dir, 'testcase')).mkdir(parents=True)

        testCaseList = []
        for testCaseFile in Path(tag, problem_path, 'testCases').iterdir():
            if (testCaseFileName := testCaseFile.parts[-1]).endswith('in'):
                testCaseOutFileName = testCaseFileName.replace('in', 'out')
                testCaseList.append({
                    'in': testCaseFileName,
                    'out': testCaseOutFileName,
                    'score': 0  # Give value later
                })
                copy(testCaseFile, Path(testCaseFolder, testCaseFileName))
                copy(Path(*testCaseFile.parts[:-1], testCaseOutFileName), Path(testCaseFolder, testCaseOutFileName))

        if str(tag) != 'Trash':
            testCaseCount = len(testCaseList)
            for i in range(testCaseCount - 1):  # Give score to test cases
                testCaseList[i]['score'] = totalScore // testCaseCount
            testCaseList[testCaseCount - 1]['score'] = totalScore // testCaseCount + totalScore % testCaseCount

        # Generate problem.json
        with Path(output_work_dir, 'problem.json').open(mode='w', encoding='utf8') as problem_JSON:
            problem_dict = \
                {
                    'display_id': str(problem_data['id']),
                    'title': problem_data['title'],
                    'description': {'format': 'html', 'value': f"<p>{problem_data['description']}</p>"},
                    'tags': [str(tag)],
                    'input_description': {'format': 'html', 'value': f"<p>{problem_data['inputFormat']}</p>"},
                    'output_description': {'format': 'html', 'value': f"<p>{problem_data['outputFormat']}</p>"},
                    'test_case_score': [
                        {'score': testCase['score'], 'input_name': testCase['in'], 'output_name': testCase['out']}
                        for testCase in testCaseList],
                    'hint': {'format': 'html', 'value': f"<p>{problem_data['hint']}</p>"},
                    'time_limit': 1000,
                    'memory_limit': 512,
                    'samples': [{'input': sample['input'], 'output': sample['output']}
                                for sample in problem_data['samples']],
                    'template': {},
                    'spj': None,
                    'rule_type': 'ACM',
                    'source': 'NTU judge girl',
                    'answers': []
                }

            dump(problem_dict, problem_JSON)

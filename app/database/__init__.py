from .models import ProblemSet, Problem, Account
from app import db
import json

db.create_all()
problemSets = ProblemSet()
problems = Problem()
accounts = Account()

p = json.load(open('./problems.json', encoding='utf-8'))
for problem in p:
    samplein = json.dumps(problem['sample_input'])
    sampleout = json.dumps(problem['sample_output'])

    if problems.search(problem['id']) == None:
        problems.insert(id=problem['id'], title=problem['title'], taskDescription=problem['description'], inputFormat=problem['input_format'], outputFormat=problem['output_format'], sampleInput=samplein, sampleOutput=sampleout, testCaseNumber=problem['test_case_number'], AC=problem['AC'], WA=problem['WA'])
    else:
        problems.update(id=problem['id'], title=problem['title'], taskDescription=problem['description'], inputFormat=problem['input_format'], outputFormat=problem['output_format'], sampleInput=samplein, sampleOutput=sampleout, testCaseNumber=problem['test_case_number'], AC=problem['AC'], WA=problem['WA'])
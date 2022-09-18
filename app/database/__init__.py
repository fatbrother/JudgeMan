from .models import ProblemSet, Problem, Account
from app import db
import json

db.create_all()
problemSets = ProblemSet()
problems = Problem()
accounts = Account()

# p = json.load(open('./problems.json', encoding='utf-8'))
# for problem in p:
#     problems.insert(id=problem['id'], title=problem['title'], description=problem['description'], input_format=problem['input_format'], output_format=problem['output_format'], sample_input=problem['sample_input'], sample_output=problem['sample_output'], hint=problem['hint'], test_case_number=problem['test_case_number'], AC=problem['AC'], WA=problem['WA'])
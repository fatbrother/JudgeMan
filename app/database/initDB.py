import os
from pathlib import Path
import json
from .models import ProblemSet, Problem, Account
from app import db

base = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute())

db.drop_all()
db.create_all()
db.session.commit()

from . import problems as p


with open(base+'\\problems.json', 'r', encoding='UTF-8') as f:
    problems = json.loads(f.read())
    for problem in problems:
        p.insert(
            id=problem['id'], 
            title=problem['title'],
            description=problem['description'],
            inputFormat=problem['inputFormat'],
            outputFormat=problem['outputFormat'],
            sampleInput=problem['sampleInput'],
            sampleOutput=problem['sampleOutput'],
            hint=problem['hint'],
            testCasePaths='[]',
            answerCasePaths='[]',
            AC=problem['AC'],
            WA=problem['WA']
        )

# with open(base+'\\problemSets.json', 'r', encoding='UTF-8') as f:
#     problemSets = json.loads(f.read())
#     for problemSet in problemSets:
#         pass

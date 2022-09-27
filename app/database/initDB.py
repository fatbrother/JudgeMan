import os
from pathlib import Path
import json
from app import db
from .models import ProblemSet, Problem

def init():
    base = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute())

    db.drop_all()
    db.create_all()
    db.session.commit()

    p = Problem()
    ps = ProblemSet()

    if os.path.exists(base+'\\problems.json'):
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
                    testCasePaths=[],
                    answerCasePaths=[],
                    AC=problem['AC'],
                    WA=problem['WA']
                )

    if os.path.exists(base+'\\problemSets.json'):
        with open(base+'\\problemSets.json', 'r', encoding='UTF-8') as f:
            problemSets = json.loads(f.read())
            for problemSet in problemSets:
                ps.insert(
                    id=problemSet['id'],
                    title=problemSet['title'],
                    problems=problemSet['problemId']
                )

    for problemSet in ps.viewAll():
        problemIds = json.loads(problemSet.problems)
        for problemId in problemIds:
            problem = p.search(problemId)
            
            testCasePaths = []
            answerCasePaths = []
            problemTitle = problem.title
            if problemTitle[-1] in '.,?!':
                problemTitle = problemTitle[:-1]
            url = base+'\\problemSet\\'+problemSet.title+'\\'+str(problem.id)+'. '+problemTitle+'\\testCases\\'

            for testCase in os.listdir(url):
                if testCase[-4:] == '.out':
                    answerCasePaths.append(testCase)
                else:
                    testCasePaths.append(testCase)

            p.update(problemId, testCasePaths=testCasePaths, answerCasePaths=answerCasePaths)
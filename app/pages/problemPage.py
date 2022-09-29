import json
import os
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user

from ..database import problems, problemSets, accounts
from ..judgeLib import judge

problem = Blueprint('problem', __name__)

@problem.route('/problemSet/<int:problemSetId>')
def index(problemSetId: int):
    session['lastPage'] = url_for('problem.index', problemSetId=problemSetId)
    problemSet = problemSets.search(problemSetId)
    problemIds = json.loads(problemSet.problems)
    subProblems = []
    for problemId in problemIds:
        problem = problems.search(problemId)
        if problem is not None:
            subProblems.append(problem)
    
    if current_user.is_authenticated:
        user = accounts.searchById(current_user.id)
        solvedProblems = json.loads(user.passProblems)

    return render_template('problemSet.html', problemSet=problemSet, subProblems=subProblems, solvedProblems=solvedProblems)


@problem.route('/problemSet/<int:problemSetId>/problem/<int:problemId>', methods=['GET', 'POST'])
def singleProblem(problemSetId: int, problemId: int, result: str = ''):
    session['lastPage'] = url_for('problem.singleProblem', problemSetId=problemSetId, problemId=problemId)

    result, input, output, answer = '', '', '', ''
    problem = problems.search(problemId)
    sampleInput = json.loads(problem.sampleInput)
    sampleOutput = json.loads(problem.sampleOutput)
    sampleLen = len(sampleInput)

    if request.method == 'POST':
        if request.form['submit']:

            if not current_user.is_authenticated:
                return redirect(url_for('account.login'))

            user = accounts.searchById(current_user.id)
            if user.level == 'Waiting':
                return 'Your account is waiting for administrator to confirm.'

            problem = problems.search(problemId)
            problemTitle = problem.title
            code = request.form['code']
            # language = request.form['language']
            language = 'c'
            testCasePaths = json.loads(problem.testCasePaths)
            answerPaths = json.loads(problem.answerCasePaths)
            acCount = problem.AC
            waCount = problem.WA
            account = accounts.searchById(current_user.id)
            passProblem = json.loads(account.passProblems)
            problemSetTitle = problemSets.search(problemSetId).title

            base = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute())
            url = base+'\\problemSet\\'+problemSetTitle+'\\'+str(problem.id)+'. '+problemTitle+'\\testCases\\'

            for testCasePath, answerPath in zip(testCasePaths, answerPaths):
                result, input, output, answer = judge(
                    code_text=code, language=language, input_dir=url+testCasePath, answer_dir=url+answerPath)

                if result != 'AC':
                    break

            if result == 'AC':
                problems.update(id=problemId, AC=acCount + 1)
                if problemId not in passProblem:
                    passProblem.append(problemId)
                    accounts.update(id=current_user.id, problems=passProblem)
            else:
                problems.update(id=problemId, WA=waCount + 1)

    return render_template('problem.html', problem=problem, sampleInput=sampleInput, sampleOutput=sampleOutput, sampleLen=sampleLen, result=result, input=input, output=output, answer=answer)

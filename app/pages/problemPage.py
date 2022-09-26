import json
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
    return render_template('problemSet.html', problemSet=problemSet, subProblems=subProblems)


@problem.route('/problemSet/<int:problemSetId>/problem/<int:problemId>', methods=['GET', 'POST'])
def singleProblem(problemSetId: int, problemId: int, result: str = ''):
    session['lastPage'] = url_for('problem.singleProblem', problemSetId=problemSetId, problemId=problemId)

    result = ''
    problem = problems.search(problemId)
    sampleInput = json.loads(problem.sampleInput)
    sampleOutput = json.loads(problem.sampleOutput)
    sampleLen = len(sampleInput)

    if request.method == 'POST':
        if request.form['submit']:

            if not current_user.is_authenticated:
                return redirect(url_for('account.login'))

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
            basicPath = 'problemSet/{}/{}/testCases/'.format(problemSetTitle, problemTitle)

            for testCasePath, answerPath in zip(testCasePaths, answerPaths):
                result, input, output, answer = judge(
                    code_text=code, language=language, input_dir=basicPath+testCasePath, answer_dir=basicPath+answerPath)

                if result != 'AC':
                    break

            if result == 'AC':
                problem.update(id=problemId, AC=acCount + 1)
                if problemId not in passProblem:
                    passProblem.append(problemId)
                    account.update(id=current_user.id, passProblem=json.dumps(passProblem))
            else:
                problem.update(id=problemId, WA=waCount + 1)

    return render_template('problem.html', problem=problem, sampleInput=sampleInput, sampleOutput=sampleOutput, sampleLen=sampleLen)

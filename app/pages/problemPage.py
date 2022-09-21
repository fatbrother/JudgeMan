import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user
from ..database import problems, problemSets, accounts
from ..judgeLib import judge

problem = Blueprint('problem', __name__)


@problem.route('/problemSet/<int:problemSetId>', methods=['GET', 'POST'])
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


@problem.route('/problem/<int:problemId>', methods=['GET', 'POST'])
def singleProblem(problemId: int, result: str = ''):
    session['lastPage'] = url_for('problem.singleProblem', problemId=problemId)
    if request.method == 'POST':
        if request.form['submit'] == 'submit':

            if not current_user.is_authenticated:
                return redirect(url_for('account.login'))

            problem = problems.search(problemId)
            code = request.form['code']
            language = request.form['language']
            testCasePaths = json.loads(problem.testCases)
            answerPaths = json.loads(problem.answers)
            ac = problem.AC
            wa = problem.WA
            account = accounts.searchById(current_user.id)
            passProblem = json.loads(account.passProblem)

            res = 'AC'
            for testCase, answer in testCasePaths, answerPaths:
                res, input, output, answer = judge(
                    code_text=code, language=language, input_dir=testCase, answer_dir=answer)

                if result != 'AC':
                    break

            if res == 'AC':
                problem.update(id=problemId, AC=ac + 1)
                if problemId not in passProblem:
                    passProblem.append(problemId)
                    account.update(id=current_user.id, passProblem=json.dumps(passProblem))
            else:
                problem.update(id=problemId, WA=wa + 1)

            return render_template('problem.html', problem=problem, result=result, sampleInput=sampleInput, sampleOutput=sampleOutput,
                                   sampleLen=sampleLen, input=input, output=output, answer=answer)

    problem = problems.search(problemId)
    sampleInput = json.loads(problem.sampleInput)
    sampleOutput = json.loads(problem.sampleOutput)
    sampleLen = len(sampleInput)
    return render_template('problem.html', problem=problem, sampleInput=sampleInput, sampleOutput=sampleOutput, sampleLen=sampleLen)

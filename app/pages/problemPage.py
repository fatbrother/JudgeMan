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

            # if user is not logged in, go to login page
            if not current_user.is_authenticated:
                return redirect(url_for('account.login'))

            problem = problems.search(problemId)
            code = request.form['code']
            language = request.form['language']
            testCases = problem.testCases
            answers = problem.answers
            AC = problem.AC
            WA = problem.WA
            account = accounts.searchById(current_user.id)
            passProblem = json.loads(account.passProblem)

            res = 'AC'
            for testCase, answer in testCases, answers:
                result, input, output, answer = judge(
                    code_text=code, language=language, input=testCase, answer=answer)

                if result == 'AC':
                    continue

                else:
                    res = result
                    break

            if res == 'AC':
                problem.update(AC=AC+1)
                if problemId not in passProblem:
                    passProblem.append(problemId)
                    account.update(passProblem=json.dumps(passProblem))
            else:
                problem.update(WA=WA+1)

            return render_template('problem.html', problem=problem, result=result, sampleInput=sampleInput, sampleOutput=sampleOutput,
                                   sampleLen=sampleLen, input=input, output=output, answer=answer)

    problem = problems.search(problemId)
    sampleInput = json.loads(problem.sampleInput)
    sampleOutput = json.loads(problem.sampleOutput)
    sampleLen = len(sampleInput)
    return render_template('problem.html', problem=problem, sampleInput=sampleInput, sampleOutput=sampleOutput, sampleLen=sampleLen)

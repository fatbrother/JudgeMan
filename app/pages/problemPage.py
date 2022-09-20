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
def singleProblem(problemId: int):
    session['lastPage'] = url_for('problem.singleProblem', problemId=problemId)
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
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

            for testCase, answer in testCases, answers:
                result, input, output, answer =  judge(code_text=code, language=language, input=testCase, answer=answer)

                if result == 'AC':
                    pass
                else:
                    WA += 1
                    problems.update(problemId, AC=AC, WA=WA)
                    return render_template('test.html', result=result, input=input, output=output, answer=answer)

            AC += 1
            passProblem.append(problemId)

            problems.update(id=id, AC=AC, WA=WA)
            accounts.update(id=current_user.id, passProblem=passProblem)

    problem = problems.search(problemId)
    sampleInput = json.loads(problem.sampleInput)
    sampleOutput = json.loads(problem.sampleOutput)
    sampleLen = len(sampleInput)
    return render_template('problem.html', problem=problem, sampleInput=sampleInput, sampleOutput=sampleOutput, sampleLen=sampleLen)

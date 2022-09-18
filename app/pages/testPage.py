from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..database import problems
from ..database import accounts
from ..judgeLib import judge
import json

test = Blueprint('test', __name__)

@test.route('/problem/<int:problemId>/test', methods=['GET', 'POST'])
@login_required
def index(problemId):
    if request.method == 'POST':
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

        
        return render_template('test.html', result='AC')

    return render_template('test.html')
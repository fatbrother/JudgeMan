from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app import db
from app.database.models import Problem
from app.database.models import Account
from app.judgeLib import judge

test = Blueprint('test', __name__)

@test.route('/problem/<int:problemId>/test', methods=['GET', 'POST'])
@login_required
def index(problemId):
    if request.method == 'POST':
        problem = Problem.query.filter_by(id=problemId).first()
        account = Account.query.filter_by(id=current_user.id).first()
        code = request.form['code']
        language = request.form['language']
        testCases = Problem.query.filter_by(id=problemId).first().input
        answers = Problem.query.filter_by(id=problemId).first().answer

        for testCase, answer in testCases, answers:
            result, input, output, answer =  judge(code_text=code, language=language, input=testCase, answer=answer)

            if result == 'AC':
                pass
            else:
                problem.WA += 1
                db.session.commit()
                return render_template('test.html', result=result, input=input, output=output, answer=answer)

        problem.AC += 1
        account.passedProblems.append(problemId)

        db.session.commit()

        
        return render_template('test.html', result='AC')

    return render_template('test.html')

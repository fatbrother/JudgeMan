from contextlib import redirect_stderr
from flask import Blueprint, render_template, request, redirect, url_for
from ..database import problems

problem = Blueprint('problem', __name__)

@problem.route('/problem/<int:problemId>', methods=['GET', 'POST'])
def index(problemId):
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            return redirect(url_for('test.index', problemId=problemId))

    problem = problems.search(problemId)
    return render_template('problem.html', problem=problem)
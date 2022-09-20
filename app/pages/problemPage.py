import json
from flask import Blueprint, render_template, request, redirect, url_for
from ..database import problems, problemSets

problem = Blueprint('problem', __name__)

@problem.route('/problemSet/<int:problemSetId>', methods=['GET', 'POST'])
def index(problemSetId: int):
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
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            return redirect(url_for('test.index', problemId=problemId))

    problem = problems.search(problemId)
    return render_template('problem.html', problem=problem)
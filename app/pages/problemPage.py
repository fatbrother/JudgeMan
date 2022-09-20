from flask import Blueprint, render_template, request, redirect, url_for
from ..database import problemSets

problem = Blueprint('problem', __name__)

@problem.route('/problemSet/<int:problemSetId>', methods=['GET', 'POST'])
def index(problemSetId: int):
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            return redirect(url_for('test.index', problemSetId=problemSetId))

    problemSet = problemSets.search(problemSetId)

    return render_template('problemSet.html', problemSet=problemSet)
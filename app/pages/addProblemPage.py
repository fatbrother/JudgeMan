from flask import Blueprint, render_template, request
from app import db

addProblem = Blueprint('addProblem', __name__)

@addProblem.route('/addProblem')
def index():
    if request.method == 'POST':
        problem = request.form['problem']
        answer = request.form['answer']
        db.problems.insert(dict(problem=problem, answer=answer))

    return render_template('addProblem.html')
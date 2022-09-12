from flask import Blueprint, render_template
from app import db

problem = Blueprint('problem', __name__)

@problem.route('/problem/<int:problemId>')
def index(problemId):
    problem = db.problems.search(id=problemId)
    return render_template('problem.html', problem=problem)